import asyncio , json 
from ..types.types import DataType , BaseType , RCD , Collation , SET




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

    def __setdatabase__(self,database:"DataBase",keys):
        self._database = database
        self.keys = tuple(map(str,keys))
        return self
        
    def __setbase__(self,new_query:str,database:"DataBase"):
        self.query = new_query
        self._database = database
        return self
    
    @property
    async def commit(self):
        await self._database.execute_commit(self.query)
    
    @property
    async def return_result(self) -> list["Base"]:
        res = await self._database.execute_return(self.query)
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
        







class Base:
    _tablename_ : str
    _database_ : "DataBase"
    _collation_ = None
    @property
    def all(self): 
        return "*"

        
    
    
    
    async def _table_creator(self,database:"DataBase"):
        if database.db.__name__ == 'asyncpg':
            self.add_all = self._add_all_pg
    
        self._database_ = database
        _foreign_keys_ = []
        _indexes_ = []
        _columns = []
        
        for column in self.__class__.__dict__.values():
            if isinstance(column,Column):        
                column._settable_(self)
                _columns.append(f"{column.column_statement}")
                                
                if any(column._foreign_key_):
                    fk = column._foreign_key_
                    if self._database_.db.__name__ == "aiosqlite":
                        q = f"FOREIGN KEY ({column.str}) REFERENCES {fk[0]._tablename_}({fk[0].str})"
                    else:
                        q = f"CONSTRAINT fk_{column.str} FOREIGN KEY ({column.str}) REFERENCES {fk[0]._tablename_}({fk[0].str})"
                        
                    if fk[2]:
                        q += " ON DELETE CASCADE"
                    if fk[1]:
                        q += " ON UPDATE CASCADE"    
                    _foreign_keys_.append(q)
                    
                                            
            
                if column._index_:
                    _indexes_.append(column)
            
            
        _columns += _foreign_keys_
        
        columns = ','.join(_columns)
        collation = ''
        if self._collation_:
            collation = f"COLLATE={self._collation_}"
        await database.execute_commit(f"CREATE TABLE IF NOT EXISTS {self._tablename_} ({columns}) {collation};")


        for c in _indexes_:
            await c.add_index()

    
    
    async def add(self,**cv):
        columns = []
        values = []
        for c,v in cv.items():
            values.append(v)
            columns.append(c)
            
        query = f"INSERT INTO {self._tablename_} ({','.join(columns)}) VALUES{tuple(values)}"     
        await self._database_.execute_commit(query)

    
    
    async def add_all(self,columns_list:list|tuple , values:list|tuple):
        query = f"INSERT INTO {self._tablename_} ({','.join([col.column for col in columns_list])}) VALUES({(self._database_._v_*len(columns_list)).removesuffix(',')})"            
        
        await self._database_.executemany_commit(query,values)
    
    async def _add_all_pg(self,columns_list:list|tuple , values:list|tuple):
        query = f"INSERT INTO {self._tablename_} ({','.join(columns_list)}) VALUES({','.join([f'${i+1}' for i in range(len(columns_list))])})"            
        await self._database_.executemany_commit(query,values)
        
    
    
    def delete(self):
        dl = DELETE(self)
        dl._database = self._database_
        return dl
    
    
    def select(self,*columns):
        return SELECT(*columns).__setdatabase__(self._database_,columns if columns and columns[0] is not SELECT.ALL else [k for k in self.__class__.__dict__.keys() if not k.startswith('_')]).FROM(self)
    
    def select_all(self,*columns):
        return SELECT_ALL(*columns).__setdatabase__(self._database_,columns if columns and columns[0] is not SELECT.ALL else [k for k in self.__class__.__dict__.keys() if not k.startswith('_')]).FROM(self)
    
    def select_distinct(self,*columns):
        return SELECT_DISTINCT(*columns).__setdatabase__(self._database_,columns if columns and columns[0] is not SELECT.ALL else [k for k in self.__class__.__dict__.keys() if not k.startswith('_')]).FROM(self)

    
    def update(self,statement)->"SELECT":
        up = UPDATE(self).SET(statement)
        up._database = self._database_
        return up


    async def drop_table(self):
        await self._database_.execute_commit(f'DROP TABLE {self._tablename_}')    
    
    async def drop_column(self,column:"Column"):
        await self._database_.execute_commit(f"ALTER TABLE {self._tablename_} DROP COLUMN {column.str}")
    
    async def drop_columns(self,*columns:"Column"):
        await self._database_.executemany_commit(';'.join([f"ALTER TABLE {self._tablename_} DROP COLUMN {column.str}" for column in columns]))
    
    async def add_column(self,column:"Column"):
        
        column._settable_(self)
        
        query = f"ALTER TABLE {self._tablename_} ADD {column.column_statement}"
    
                
        if any(column._foreign_key_) and self._database_.db.__name__ != 'aiosqlite':
            fk = column._foreign_key_
            query += f",ADD CONSTRAINT fk_{column.str} FOREIGN KEY ({column.str}) REFERENCES {fk[0]._tablename_}({fk[0].str})"
            if fk[2]:
                query += " ON DELETE CASCADE"
            if fk[1]:
                query += " ON UPDATE CASCADE"
                    
        
        await self._database_.execute_commit(query)
        
        if any(column._foreign_key_) and self._database_.db.__name__ == 'aiosqlite':
            await column.add_foreign_key(column._foreign_key_)
        
        if column._index_:
            await column.add_index()    
        
        
    
    
    
    async def add_index(self,column:"Column"):
        await column.add_index()
        
    async def add_foreign_key(self,column:"Column",reference_column:"Column",on_update:bool=None,on_delete:bool=None):
        await column.add_foreign_key(reference_column,on_update,on_delete)

    async def rename_column(self,column:"Column",new_name:str):
        await column.rename(new_name)
    
    async def rename_table(self,new_name:str):
        query = f"ALTER TABLE {self._tablename_} RENAME TO {new_name}"
        await self._database_.execute_commit(query)
        self._tablename_ = new_name
        for column in self.__class__.__dict__.values():
            if isinstance(column,Column):        
                column._tablename_ = new_name
    
    

    
    
    def __str__(self):
        return self._tablename_    

    def __repr__(self):
        return json.dumps(self.__dict__,default=str,indent=4)



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
            self._v_ = '%s,'
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
            self._v_ = '?,'
            if self.timeout :
                self.kwargs['timeout'] = self.timeout
            database = f"{self.database_name.removesuffix('.db')}.db"
            if self.path:
                database = f"{self.path.removesuffix('/')}/{database}"
            self._pool = [await self.db.connect(
                database = database,
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
        con = await self._pop()                                
        async with await con.cursor() as cur:
            await cur.execute(str(query),values)
            await con.commit()
    
        self._pool.append(con)


    async def execute_return(self,query:str,values:tuple=()) -> list[tuple] :
        con = await self._pop()                               
                         
        async with await con.cursor() as cur:
            await cur.execute(str(query),values)
            res = await cur.fetchall()
            
        self._pool.append(con)
        return res
        
    async def executemany_commit(self,query:str,values:tuple=()):
        con = await self._pop()        
        async with await con.cursor() as cur:
            await cur.executemany(str(query),values)
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
    
    async def _close_pool(self):
        for con in self._pool:
            await con.close()



