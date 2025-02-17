import asyncio , json 
from ..types.types import DataType , BaseType , RCD , Collation , SET


class ColumnBase:
    
    __pr__ = ''
    __su__ = ''
    
    def __init__(self,v:"DataType",c):
        self.__string__= f"{c}"
        self.__pr__ = v.__pr__
        self.__su__ = v.__su__
    
    
    
    
    @property
    def str(self):
        return self.__string__
    
    
    def __str__(self):
        return self.__string__
    
    def __repr__(self):
        return self.__string__
    
    
    def __eq__(self, value):
        return BaseType(
            self.__string__+ f' = {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __ne__(self, value):
        return BaseType(
            self.__string__+ f' != {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)
    
    def  __gt__(self,value):
        return BaseType(
        self.__string__+ f' > {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __lt__(self,value):
        return BaseType(
        self.__string__+ f' < {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def  __ge__(self,value):
        return BaseType(
        self.__string__+ f' >= {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __le__(self,value):
        return BaseType(
        self.__string__+ f' <= {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __or__(self, value):
        return BaseType(
        self.__string__+ f' OR {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __and__(self,value):
        return BaseType(
        self.__string__+ f' AND {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __add__(self, value):
        return BaseType(
        self.__string__+ f' + {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __sub__(self, value):
        return BaseType(
        self.__string__+ f' - {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __mul__(self, value):
        return BaseType(
        self.__string__+ f' * {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __truediv__(self, value):
        return BaseType(
            self.__string__+ f' / {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)
                
    def __floordiv__(self, value):
        return BaseType(
        self.__string__+ f' // {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __mod__(self, value):
        return BaseType(
        self.__string__+ f' % {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)

    def __pow__(self, value):
        return BaseType(
        self.__string__+ f' ** {self.__pr__}{value}{self.__su__}',
            self.__pr__,
            self.__su__)
        
    def __contains__(self,value):
        return BaseType(
            f' {value} IN {self.__string__}',
            self.__pr__,
            self.__su__) 

    def IN(self,set:"SET"):
        return BaseType(set.contains(self),
            self.__pr__,
            self.__su__) 

    def NOT_IN(self,set:"SET"):
        return BaseType(set.not_contains(self),
            self.__pr__,
            self.__su__) 
                        
    @property
    def IS_NULL(self):
        return BaseType(f"{self} IS NULL",
            self.__pr__,
            self.__su__) 
    
    @property
    def IS_NOT_NULL(self):
        return BaseType(f"{self} IS NOT NULL",
            self.__pr__,
            self.__su__) 
    
    def IS(self,item):
        return BaseType(f"{self} IS {item}",
            self.__pr__,
            self.__su__) 
    
    def BETWEEN(self,a,b):
        return BaseType(f"BETWEEN {a.__repr__()} AND {b.__repr__()}",
            self.__pr__,
            self.__su__) 

    def LIKE(self,statement:str):
        return BaseType(f"{self} LIKE {statement.__repr__()}",
            self.__pr__,
            self.__su__)
    
    def AS(self,new_name):
        self.__string__ += f" AS {new_name}"
        return self
        
        

    
class Column(ColumnBase):
    __tablename__ : str
    __index__ = None
    __foreign_key__ = None


    async def drop_column(self):
        await self._database_.execute_commit(f"ALTER TABLE {self.__tablename__} DROP COLUMN {self.str}")

    async def drop_index(self,index_name=None):
        await self._database_.execute_commit(f"DROP INDEX idx_{self.str} ON {self.__tablename__}")

    async def add_index(self):
        query = f"ALTER TABLE {self.__tablename__} ADD INDEX idx_{self.str} ({self.str})"
        await self._database_.execute_commit(query)
    
    async def add_foreign_key(self,reference_column:"Column"):
        query = f"ALTER TABLE {self.__tablename__} ADD CONSTRAINT fk_{self.str} FOREIGN KEY ({self.str}) REFERENCES {reference_column.__tablename__}({reference_column.str})"
        await self._database_.execute_commit(query)


    async def rename(self,new_name):
        query = f"ALTER TABLE {self.__tablename__} CHANGE {self.column} {new_name} {self.datatype.TYPE}"
        await self._database_.execute_commit(query)
        self.column = new_name

        

    
    @property
    def str(self):
        return self.column
    
    def __repr__(self):
        return self.column

    def __str__(self):
        return f"{self.__tablename__}.{self.column}"


    def __settable__(self,table):
        self.__tablename__ = table.__tablename__
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
                 index :bool= None,
                 collation : Collation = None,
                 comment :str = None
                 ):
        self.__index__ = index
        self.__foreign_key__ = foreign_key
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

    def __setdatabase__(self,database:"DataBase",keys):
        self.__database = database
        self.keys = keys
        return self
        
    def __setbase__(self,new_query:str,database:"DataBase"):
        self.query = new_query
        self.__database = database
        return self
    
    @property
    async def commit(self):
        await self.__database.execute_commit(self.query)
    
    @property
    async def return_result(self) -> list["Base"]:
        res = await self.__database.execute_return(self.query)
        if not res:
            return res

        return [RCD(**dict(zip(self.keys,v))) for v in res]
    
        
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
        columns = ', '.join(columns)
        self.query += f" ORDER BY {columns} {order}"
        return self
   
    def GROUP_BY(self,*columns):
        columns = ', '.join(columns)
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

    def SET(self,statement):
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
    
    def DROP_COLUMN(self,table:"Base",column:"Column"):
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



class WHERE(SELECT):
    def __init__(self,statement):
        super().__init__()
        self.query = f'{statement}'
        







class Base:
    __tablename__ : str
    _database_ : "DataBase"
    __foreign_keys__ = []
    __indexes__ = []
    __collation__ = None
    @property
    def all(self): 
        return "*"

    def _foreign_key(self,column,anothor_column):
        self.__foreign_keys__.append(f"FOREIGN KEY ({column.str}) REFERENCES {anothor_column.__tablename__}({anothor_column.str})")
            
    
    def _add_index(self,column:"Column"):
        self.__indexes__.append(f"INDEX idx_{column.str} ({column.str})")
    
    
    async def _table_creator(self,database:"DataBase"):
        self._database_ = database
        
        _columns = []
        for column in self.__class__.__dict__.values():
            if isinstance(column,Column):        
                column.__settable__(self)
                _columns.append(f"{column.column_statement}")
                
                if column.__foreign_key__:
                    self._foreign_key(column,column.__foreign_key__)
            
                if column.__index__:
                    self._add_index(column)
                
       
        _columns += self.__foreign_keys__
        _columns += self.__indexes__
        columns = ','.join(_columns)
        collation = ''
        if self.__collation__:
            collation = f"COLLATE={self.__collation__}"
        await database.execute_commit(f"CREATE TABLE IF NOT EXISTS {self.__tablename__} ({columns}) {collation};")
    
    
    
    async def add(self,**cv):
        columns = []
        values = []
        for c,v in cv.items():
            values.append(v)
            columns.append(c)
            
        query = f"INSERT INTO {self.__tablename__} ({','.join(columns)}) VALUES{tuple(values)}"     
        await self._database_.execute_commit(query)

    
    
    async def add_all(self,*add_list):
        query = ''
        values = []
        for cv in add_list:
            columns = []
            for c,v in cv.items():
                values.append(v)
                columns.append(c)
                
            query += f"INSERT INTO {self.__tablename__} ({','.join(columns)}) VALUES{tuple(values)};"     
        
        await self._database_.executemulti_commit(query)
    
    
    
    def delete(self):
        return SELECT().__setbase__(f"DELETE FROM {self.__tablename__}",self._database_)
    
    
    def select(self,*columns):
        return SELECT(*columns).__setdatabase__(self._database_,columns if columns and columns[0] is not SELECT.ALL else [k for k in self.__class__.__dict__.keys() if not k.startswith('_')]).FROM(self)
    
    def select_all(self,*columns):
        return SELECT_ALL(*columns).__setdatabase__(self._database_,columns if columns and columns[0] is not SELECT.ALL else [k for k in self.__class__.__dict__.keys() if not k.startswith('_')]).FROM(self)
    
    def select_distinct(self,*columns):
        return SELECT_DISTINCT(*columns).__setdatabase__(self._database_,columns if columns and columns[0] is not SELECT.ALL else [k for k in self.__class__.__dict__.keys() if not k.startswith('_')]).FROM(self)

    
    def update(self,statement)->"SELECT":
        return SELECT().__setbase__(f'UPDATE {self.__tablename__} SET {statement}',self._database_)


    async def drop_table(self):
        await self._database_.execute_commit(f'DROP TABLE {self.__tablename__}')    
    
    async def drop_column(self,column:"Column"):
        await self._database_.execute_commit(f"ALTER TABLE {self.__tablename__} DROP COLUMN {column.str}")
    
    async def drop_columns(self,*columns:"Column"):
        await self._database_.executemulti_commit(';'.join([f"ALTER TABLE {self.__tablename__} DROP COLUMN {column.str}" for column in columns]))
    
    async def add_column(self,column:"Column"):
        column.__settable__(self)
        
        query = f"ALTER TABLE {self.__tablename__} ADD {column.column_statement}"
    
        if column.__index__:
            query += f",ADD INDEX idx_{column.str} ({column.str})"
                
        if column.__foreign_key__:
            query += f",ADD CONSTRAINT fk_{column.str} FOREIGN KEY ({column.str}) REFERENCES {column.__foreign_key__.__tablename__}({column.__foreign_key__.str})"
    
        
        await self._database_.execute_commit(query)
    
    
    
    
    async def add_index(self,column:"Column"):
        await column.add_index()
        
    async def add_foreign_key(self,column:"Column",reference_column:"Column"):
        await column.add_foreign_key(reference_column)

    async def rename_column(self,column:"Column",new_name:str):
        await column.rename(new_name)
    
    async def rename_table(self,new_name:str):
        query = f"ALTER TABLE {self.__tablename__} RENAME TO {new_name}"
        await self._database_.execute_commit(query)
        self.__tablename__ = new_name
        for column in self.__class__.__dict__.values():
            if isinstance(column,Column):        
                column.__tablename__ = new_name
    
    

    
    
    def __str__(self):
        return self.__tablename__    

    def __repr__(self):
        return json.dumps(self.__dict__,indent=4)



class DataBase:
    # name : str
    # username : str
    # password : str
    # host : str

    def __init__(self,
                 db,
                 host='127.0.0.1',
                 user='root',
                 password='',
                 database_name='test',
                 path ='',
                 pool_size:int=5,
                 port=None,
                 unix_socket=None,
                 charset='',
                 sql_mode=None,
                 read_default_file=None,
                 use_unicode=None,
                 client_flag=0,
                 init_command=None,
                 timeout=None,
                 read_default_group=None,
                 autocommit=False,
                 echo=False,
                 local_infile=False,
                 loop=None,
                 ssl=None,
                 auth_plugin='',
                 program_name='',
                 server_public_key=None,
                                  
                 dsn=None,
                 passfile=None,
                 statement_cache_size=100,
                 max_cached_statement_lifetime=300,
                 max_cacheable_statement_size=1024 * 15,
                 command_timeout=None,
                 direct_tls=None,
                 server_settings=None,
                 target_session_attrs=None,
                 krbsrvname=None,
                 gsslib=None,
                
                 
                 iter_chunk_size=64,    
                 **kwargs
                 ):
        self.db = db
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host 
        self.pool_size = pool_size
        self.port=port
        self.unix_socket=unix_socket
        self.charset=charset
        self.sql_mode=sql_mode
        self.read_default_file=read_default_file
        self.use_unicode=use_unicode
        self.client_flag=client_flag
        self.init_command=init_command
        self.timeout=timeout
        self.read_default_group=read_default_group
        self.autocommit=autocommit
        self.echo=echo
        self.local_infile=local_infile
        self.ssl=ssl
        self.auth_plugin=auth_plugin
        self.program_name=program_name
        self.server_public_key=server_public_key

        self.dsn=dsn,
        self.passfile=passfile,
        self.statement_cache_size=statement_cache_size,
        self.max_cached_statement_lifetime=max_cached_statement_lifetime,
        self.max_cacheable_statement_size=max_cacheable_statement_size,
        self.command_timeout=command_timeout,
        self.direct_tls=direct_tls,
        self.server_settings=server_settings,
        self.target_session_attrs=target_session_attrs,
        self.krbsrvname=krbsrvname,
        self.gsslib=gsslib,
        
        self.loop=loop        
        self.path = path
        self.iter_chunk_size=iter_chunk_size
        
        self.kwargs = kwargs
    
    
    def create(self,*tabels):
        asyncio.get_event_loop().run_until_complete(self._create(*tabels))
        return self
    

    async def _create_database(self,connection):
        query = f'CREATE DATABASE IF NOT EXISTS {self.database_name}'
        async with await connection as con:
            async with await con.cursor() as cur:
                await cur.execute(query)
                await con.commit()


     
    async def _create(self,*tabels:Base):
        if self.db.__name__ == 'aiomysql':
            await self._create_database(self.db.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port or 3306,
                unix_socket=self.unix_socket,
                charset=self.charset,
                sql_mode=self.sql_mode,
                read_default_file=self.read_default_file,
                use_unicode=self.use_unicode,
                client_flag=self.client_flag,
                init_command=self.init_command,
                connect_timeout=self.timeout,
                read_default_group=self.read_default_file,
                autocommit=self.autocommit,
                echo=self.echo,
                local_infile=self.local_infile,
                loop=self.loop,
                ssl=self.ssl,
                auth_plugin=self.auth_plugin,
                program_name=self.program_name,
                server_public_key=self.server_public_key
                ))
            self._pool = [await self.db.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                db=self.database_name,        
                port=self.port or 3306,
                unix_socket=self.unix_socket,
                charset=self.charset,
                sql_mode=self.sql_mode,
                read_default_file=self.read_default_file,
                use_unicode=self.use_unicode,
                client_flag=self.client_flag,
                init_command=self.init_command,
                connect_timeout=self.timeout,
                read_default_group=self.read_default_file,
                autocommit=self.autocommit,
                echo=self.echo,
                local_infile=self.local_infile,
                loop=self.loop,
                ssl=self.ssl,
                auth_plugin=self.auth_plugin,
                program_name=self.program_name,
                server_public_key=self.server_public_key
                ) for _ in range(self.pool_size)]
        
        elif self.db.__name__ == 'aiosqlite':
            if self.timeout :
                self.kwargs['timeout'] = self.timeout
            
            self._pool = [await self.db.connect(
                database = f"{self.path.removesuffix('/')}/{self.database_name.removesuffix('.db')}.db",
                loop = self.loop,
                iter_chunk_size= self.iter_chunk_size,
                **self.kwargs
                ) for _ in range(self.pool_size)]
        
        elif self.db.__name__ == 'asyncpg':
            await self._create_database(self.db.connect(
                dsn=self.dsn,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                passfile=self.passfile,
                database=self.database_name,
                loop=self.loop,
                timeout=self.timeout or 60,
                statement_cache_size=self.statement_cache_size,
                max_cached_statement_lifetime=self.max_cached_statement_lifetime,
                max_cacheable_statement_size=self.max_cacheable_statement_size,
                command_timeout=self.command_timeout,
                ssl=self.ssl,
                direct_tls=self.direct_tls,
                server_settings=self.server_settings,
                target_session_attrs=self.target_session_attrs,
                krbsrvname=self.krbsrvname,
                gsslib=self.gsslib
            ))
        
            self._pool = [await self.db.connect(
                dsn=self.dsn,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                passfile=self.passfile,
                database=self.database_name,
                loop=self.loop,
                timeout=self.timeout or 60,
                statement_cache_size=self.statement_cache_size,
                max_cached_statement_lifetime=self.max_cached_statement_lifetime,
                max_cacheable_statement_size=self.max_cacheable_statement_size,
                command_timeout=self.command_timeout,
                ssl=self.ssl,
                direct_tls=self.direct_tls,
                server_settings=self.server_settings,
                target_session_attrs=self.target_session_attrs,
                krbsrvname=self.krbsrvname,
                gsslib=self.gsslib
            ) for _ in range(self.pool_size)]
            
            
        else:
            raise Exception('Database Invauled')
        
        for t in tabels: await t._table_creator(self)
        

    async def execute_commit(self,query:str,values:tuple=()):
        print(query)
        print('----------------------------')
        con = await self._pop()                                
        async with await con.cursor() as cur:
            await cur.execute(query,values)
            await con.commit()
    
        self._pool.append(con)


    async def execute_return(self,query:str,values:tuple=()) -> list[tuple] :
        print(query)
        print('----------------------------')
        con = await self._pop()                               
                         
        async with await con.cursor() as cur:
            await cur.execute(query,values)
            res = await cur.fetchall()
            
        self._pool.append(con)
        return res
        
    async def executemulti_commit(self,query:str,values:tuple=()):
        print(query)
        print('----------------------------')
        con = await self._pop()        
        async with await con.cursor() as cur:
            async for _ in cur.executemulti(query,values):pass
            await con.commit()
        
        self._pool.append(con)

    async def _pop(self):
        try:
            return self._pool.pop()
        except:
            while True:
                await asyncio.sleep(0.001)
                try:
                    return self._pool.pop()
                except:pass
        


