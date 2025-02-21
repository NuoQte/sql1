from ..types import DataType , BaseType, SET , Collation ,RCD

class ColumnBase:
    
    _pr_ = ''
    _su_ = ''
    
    def __init__(self,v:"DataType",c):
        self._string_= f"{c}"
        self._pr_ = v._pr_
        self._su_ = v._su_
    
    
    
    
    @property
    def str(self):
        return self._string_
    
    
    def __str__(self):
        return self._string_
    
    def __repr__(self):
        return self._string_
    
    
    def __eq__(self, value):
        return BaseType(
            self._string_+ f' = {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __ne__(self, value):
        return BaseType(
            self._string_+ f' != {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)
    
    def  __gt__(self,value):
        return BaseType(
        self._string_+ f' > {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __lt__(self,value):
        return BaseType(
        self._string_+ f' < {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def  __ge__(self,value):
        return BaseType(
        self._string_+ f' >= {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __le__(self,value):
        return BaseType(
        self._string_+ f' <= {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __or__(self, value):
        return BaseType(
        self._string_+ f' OR {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __and__(self,value):
        return BaseType(
        self._string_+ f' AND {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __add__(self, value):
        return BaseType(
        self._string_+ f' + {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __sub__(self, value):
        return BaseType(
        self._string_+ f' - {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __mul__(self, value):
        return BaseType(
        self._string_+ f' * {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __truediv__(self, value):
        return BaseType(
            self._string_+ f' / {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)
                
    def __floordiv__(self, value):
        return BaseType(
        self._string_+ f' // {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __mod__(self, value):
        return BaseType(
        self._string_+ f' % {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)

    def __pow__(self, value):
        return BaseType(
        self._string_+ f' ** {self._pr_}{value}{self._su_}',
            self._pr_,
            self._su_)
        
    def __contains__(self,value):
        return BaseType(
            f' {value} IN {self._string_}',
            self._pr_,
            self._su_) 

    def IN(self,set:"SET"):
        return BaseType(set.contains(self),
            self._pr_,
            self._su_) 

    def NOT_IN(self,set:"SET"):
        return BaseType(set.not_contains(self),
            self._pr_,
            self._su_) 
                        
    @property
    def IS_NULL(self):
        return BaseType(f"{self} IS NULL",
            self._pr_,
            self._su_) 
    
    @property
    def IS_NOT_NULL(self):
        return BaseType(f"{self} IS NOT NULL",
            self._pr_,
            self._su_) 
    
    def IS(self,item):
        return BaseType(f"{self} IS {item}",
            self._pr_,
            self._su_) 
    
    def BETWEEN(self,a,b):
        return BaseType(f"BETWEEN {a.__repr__()} AND {b.__repr__()}",
            self._pr_,
            self._su_) 

    def LIKE(self,statement:str):
        return BaseType(f"{self} LIKE {statement.__repr__()}",
            self._pr_,
            self._su_)
    
    def AS(self,new_name):
        self._string_ += f" AS {new_name}"
        return self
        
        

    
class Column(ColumnBase):
    _tablename_ : str
    _index_ = None
    _foreign_key_ = []


    async def drop_column(self):
        await self._database_.execute_commit(f"ALTER TABLE {self._tablename_} DROP COLUMN {self.str}")

    async def drop_index(self,index_name=None):
        await self._database_.execute_commit(f"DROP INDEX idx_{self.str} ON {self._tablename_}")

    async def add_index(self):
        # query = f"ALTER TABLE {self._tablename_} ADD INDEX idx_{self.str} ({self.str})"
        query = f"CREATE INDEX IF NOT EXISTS idx_{self.str} ON {self._tablename_} ({self.str})"
        await self._database_.execute_commit(query)
    
    async def add_foreign_key(self,reference_column:"Column",on_update :bool=None,on_delete:bool=None):
        query = f"ALTER TABLE {self._tablename_} ADD CONSTRAINT fk_{self.str} FOREIGN KEY ({self.str}) REFERENCES {reference_column._tablename_}({reference_column.str})"
        if on_delete:
            query += " ON DELETE CASCADE"
        if on_update:
            query += " ON UPDATE CASCADE"
        await self._database_.execute_commit(query)


    async def rename(self,new_name):
        query = f"ALTER TABLE {self._tablename_} CHANGE {self.column} {new_name} {self.datatype.TYPE}"
        await self._database_.execute_commit(query)
        self.column = new_name

        

    
    @property
    def str(self):
        return self.column
    
    def __repr__(self):
        return self.column

    def __str__(self):
        return f"{self._tablename_}.{self.column}"


    def _settable_(self,table):
        
        self._tablename_ = table._tablename_
        self._database_ = table._database_
        
    def __init__(self,
                 column_name :"str",
                 datatype :"DataType",
                 default =None,
                 not_null :bool =None,
                 primary_key :bool =None,
                 unique :bool =None,
                 auto_increment :bool =None,
                 autoincrement:bool =None,
                 serial :bool =None,
                 foreign_key :"Column"= None,
                 foreign_key_on_update :bool= None,
                 foreign_key_on_delete :bool= None,
                 index :bool= None,
                 collation : Collation = None,
                 comment :str = None
                 ):
        self._index_ = index
        self._foreign_key_ = (foreign_key,foreign_key_on_update,foreign_key_on_delete)
        self.column = column_name
        self.datatype = datatype
        self.column_statement = f"{column_name} {datatype.TYPE}"
        if auto_increment:
            self.column_statement += " AUTO_INCREMENT"
        if serial:
            self.column_statement += " SERIAL"
        if primary_key:
            self.column_statement += " PRIMARY KEY"
        if autoincrement:
            self.column_statement += " AUTOINCREMENT"
        if default:
            self.column_statement += f" DEFAULT {default}"
        if not_null:
            self.column_statement += " NOT NULL"
        if unique:
            self.column_statement += " UNIQUE"
        if collation:
            self.column_statement += f" COLLATE {collation}"
        if comment:
            self.column_statement += f" COMMENT '{comment}'"
        
        
        super().__init__(datatype,column_name)
    

class SELECT:
    query = "SELECT "
    ALL = Column('*',DataType)
    
    @property
    def str(self):
        return self.ALL
    
    
    def __init__(self,*columns):
        
        if not columns:
            self.query += "*"
        else:
            self.query += ','.join(map(str,columns))

    def __setdatabase__(self,database,keys):
        self._database = database
        self.keys = tuple(map(str,keys))
        return self
        
    def __setbase__(self,new_query:str,database):
        self.query = new_query
        self._database = database
        return self
    
    @property
    async def commit(self):
        await self._database.execute_commit(self.query)
    
    @property
    async def return_result(self) -> list:
        res = await self._database.execute_return(self.query)
        if res:
            return [RCD(**dict(zip(self.keys,v))) for v in res]
        
        return res
        
    
        
    def __str__(self):
        return self.query
    def __repr__(self):
        return self.query
        
    
    def FROM(self,table):
        self.query += f' FROM {table}'
        return self
    
    def WHERE(self,statement=""):
        self.query += f' WHERE {statement}'
        return self
    
    def AND(self,statement):
        self.query += f' AND {statement}'
        return self
    
    def OR(self,statement):
        self.query += f' OR {statement}'
        return self
    
    def NOT(self,statement):
        self.query += f' NOT {statement}'
        return self

    def UNION(self,statement:"SELECT"):
        self.query += f" UNION {statement}"
        return self
        

    def UNION_ALL(self,statement:"SELECT"):
        self.query += f" UNION ALL {statement}"
        return self

    def INTERSECT(self,statement:"SELECT"):
        self.query += f" INTERSECT {statement}"
        return self

    def EXCEPT(self,statement:"SELECT"):
        self.query += f" EXCEPT {statement}"
        return self

    def ORDER_BY(self,*columns,order="ASC"):
        columns = ', '.join(map(str,columns))
        self.query += f" ORDER BY {columns} {order}"
        return self
   
    def GROUP_BY(self,*columns):
        columns = ', '.join(map(str,columns))
        self.query += f" GROUP BY {columns}"
        return self
    
    def HAVING(self,statement=""):
        self.query += f' HAVING {statement}'
        return self

    def JOIN(self,statement):
        self.query += f" JOIN {statement}"
        return self

    def ON(self,statement):
        self.query += f" ON {statement}"
        return self


    def INNER_JOIN(self,statement):
        self.query += f" INNER JOIN {statement}"
        return self

    def LEFT_JOIN(self,statement):
        self.query += f" LEFT JOIN {statement}"
        return self

    def RIGHT_JOIN(self,statement):
        self.query += f" RIGHT JOIN {statement}"
        return self

    def FULL_OUTER_JOIN(self,statement):
        self.query += f" FULL OUTER JOIN {statement}"
        return self

    def FULL_JOIN(self,statement):
        self.query += f" FULL JOIN {statement}"
        return self

    def CROSS_JOIN(self,statement):
        self.query += f" CROSS JOIN {statement}"
        return self


    def LEFT_OUTER_JOIN(self,statement):
        self.query += f" LEFT OUTER JOIN {statement}"
        return self

    def RIGHT_OUTER_JOIN(self,statement):
        self.query += f" RIGHT OUTER JOIN {statement}"
        return self

    @property
    def parenthesize_query(self):
        self.query = f"({self.query})"
        return self
    
    def AS(self,new_name):
        self.query += f" AS {new_name}"
        return self

    def LIMIT(self,statement):
        self.query += f" LIMIT {statement}"
        return self
    
    def LIMIT_OFFSET(self,a,b):
        self.query += f" LIMIT {a} OFFSET {b}"
        return self
    
    def BY(self,statement):
        self.query += f" BY {statement}"
        return self

    def SET(self,**kv):
        statement = ",".join([f"{k} = {v}" for k,v in kv.items()])
        self.query += f" SET {statement}"
        return self
    
    def VALUES(self,*values):
        self.query += f" VALUES ({tuple(values).__repr__()})"
        return self
    
    def DROP_TABLE(self,table):
        self.query += f" DROP TABLE {table}"
        return self
    
    def DROP_DATABASE(self,db_name):
        self.query += f" DROP DATABASE {db_name}"
        return self
    
    def DROP_INDEX(self,table,index_name):
        self.query += f" DROP INDEX {index_name} ON {table}"
        return self
    
    def DROP_COLUMN(self,table,column:"Column"):
        self.query += f" ALTER TABLE {table} DROP COLUMN {column.str}"
        return self
    
    def DROP_VIEW(self,view_name):
        self.query += f" DROP VIEW {view_name}"
        return self
    
    def DROP_PROCEDURE(self,procedure_name):
        self.query += f" DROP PROCEDURE {procedure_name}"
        return self
    
    def DROP_FUNCTION(self,functin_name):
        self.query += f" DROP FUNCTION {functin_name}"
        return self
    
    def DROP_EVENT(self,event_name):
        self.query += f" DROP EVENT {event_name}"
        return self
    
    def DROP_TRIGGER(self,trigger_name):
        self.query += f" DROP TRIGGER {trigger_name}"
        return self
        



class SELECT_DISTINCT(SELECT):
    query = "SELECT DISTINCT "


class SELECT_ALL(SELECT):
    query = "SELECT ALL "



class DELETE(SELECT):
    def __init__(self, table):
        super().__init__()
        self.query = f"DELETE FROM {table}"

class UPDATE(SELECT):
    def __init__(self, table):
        super().__init__()
        self.query = f"UPDATE {table}"

class WHERE(SELECT):
    def __init__(self,statement):
        super().__init__()
        self.query = f'{statement}'
