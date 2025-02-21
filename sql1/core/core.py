import asyncio , json 
from ..sql_class import Column,DELETE , SELECT ,SELECT_ALL,SELECT_DISTINCT ,UPDATE


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

    
    def update(self,**kv)->"UPDATE":
        up = UPDATE(self).SET(**kv)
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



