from types import SimpleNamespace 
import json

class RCD(SimpleNamespace):
    

    def _default(self,v):
        if v.__class__.__name__ == "Decimal":
            return float(v)
        
        return str(v)
        
    def __repr__(self):
        return json.dumps(self.__dict__,default=self._default,indent=4)

    def __str__(self):
        return json.dumps(self.__dict__,default=self._default,indent=4)


class BaseType:
    
    _pr_ = ''
    _su_ = ''
    
    def __init__(self,string="",pr="",su=""):
        self._string_= f"{string}"
        self._pr_ = pr
        self._su_ = su
    
    def __str__(self):
        return self._string_
    
    def __repr__(self):
        return self._string_
    
    
    def __eq__(self, value):
        self._string_+= f' = {self._pr_}{value}{self._su_}'
        return self

    def __ne__(self, value):
        self._string_+= f' != {self._pr_}{value}{self._su_}'
        return self
    
    def  __gt__(self,value):
        self._string_+= f' > {self._pr_}{value}{self._su_}'
        return self
    def __lt__(self,value):
        self._string_+= f' < {self._pr_}{value}{self._su_}'
        return self
    def  __ge__(self,value):
        self._string_+= f' >= {self._pr_}{value}{self._su_}'
        return self
    def __le__(self,value):
        self._string_+= f' <= {self._pr_}{value}{self._su_}'
        return self
    def __or__(self, value):
        self._string_+= f' OR {self._pr_}{value}{self._su_}'
        return self
    def __and__(self,value):
        self._string_+= f' AND {self._pr_}{value}{self._su_}'
        return self
    def __add__(self, value):
        self._string_+= f' + {self._pr_}{value}{self._su_}'
        return self
    def __sub__(self, value):
        self._string_+= f' - {self._pr_}{value}{self._su_}'
        return self
    def __mul__(self, value):
        self._string_+= f' * {self._pr_}{value}{self._su_}'
        return self

    def __truediv__(self, value):
        self._string_+= f' / {self._pr_}{value}{self._su_}'
        return self
                
    def __floordiv__(self, value):
        self._string_+= f' // {self._pr_}{value}{self._su_}'
        return self
    def __mod__(self, value):
        self._string_+= f' % {self._pr_}{value}{self._su_}'
        return self
    def __pow__(self, value):
        self._string_+= f' ** {self._pr_}{value}{self._su_}'
        return self

    
    def __contains__(self,value):
        self._string_+= f' {value} IN {self._string_}' 
        return self


class DataType:
    _pr_ = ""
    _su_ = ""
    TYPE :str = None
    
    def __str__(self):
        return self.TYPE
    def __repr__(self):
        return self.TYPE



class VARCHAR(DataType):
    _pr_ = "'"
    _su_ = "'"
    def __init__(self,n):
        self.TYPE = f'VARCHAR({n})'

class CHAR(DataType):
    _pr_ = "'"
    _su_ = "'"
    def __init__(self,n):
        self.TYPE = f'CHAR({n})'

class TEXT(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "TEXT"

class TINYTEXT(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "TINYTEXT"

class MEDIUMTEXT(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "MEDIUMTEXT"

class LONGTEXT(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "LONGTEXT"

class BLOB(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "BLOB"

class TINYBLOB(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "TINYBLOB"

class MEDIUMBLOB(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "MEDIUMBLOB"

class LONGBLOB(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "LONGBLOB"

class BINARY(DataType):
    _pr_ = "'"
    _su_ = "'"
    def __init__(self,v):
        self.TYPE = f"BINARY({v})"
    
class VARBINARY(DataType):
    _pr_ = "'"
    _su_ = "'"
    def __init__(self,v):
        self.TYPE = f"VARBINARY({v})"


class DATE(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "DATE"

class DATETIME(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "DATETIME"


class TIME(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "TIME"


class TIMESTAMP(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "TIMESTAMP"


CURRENT_TIMESTAMP = "CURRENT_TIMESTAMP"

class YEAR(DataType):
    _pr_ = "'"
    _su_ = "'"
    TYPE = "YEAR"


class INT(DataType):
    TYPE = 'INT'

class INTEGER(DataType):
    TYPE = 'INTEGER'

class TINYINT(DataType):
    def __init__(self,v):
        self.TYPE = f'TINYINT({v})'


class SMALLINT(DataType):
    def __init__(self,v):
        self.TYPE = f'SMALLINT({v})'

class MEDIUMINT(DataType):
    def __init__(self,v):
        self.TYPE = f'MEDIUMINT({v})'

class BIGINT(DataType):
    def __init__(self,v):
        self.TYPE = f'BIGINT({v})'
        

class FLOAT(DataType):
    def __init__(self,a,b):
        self.TYPE = f"FLOAT({a},{b})"
    

class DOUBLE(DataType):
    def __init__(self,a,b):
        self.TYPE = f"DOUBLE({a},{b})"
    
    
class DECIMAL(DataType):
    def __init__(self,a,b):
        self.TYPE = f"DECIMAL({a},{b})"
    
class REAL(DataType):
    TYPE = "REAL"


class SET(DataType):
    TYPE = 'SET'
    def __init__(self,s:tuple):
        self.set = tuple(s).__repr__()
        
    def contains(self,item):
        return f"{item.__repr__()} IN {self.set}"
    
    def not_contains(self,item):
        return f"{item.__repr__()} NOT IN {self.set}"
    

class NULL(DataType):
    TYPE = "NULL"


class BOOLEAN(DataType):
    TYPE = "BOOLEAN"

class ENUM(DataType):
    _pr_ = "'"
    _su_ = "'"
    def __init__(self,set:tuple[str]):
        self.TYPE = f"ENUM{set.__repr__()}"



class Collation:
    utf8_bin = "utf8_bin"
    utf8mb4_bin = "utf8mb4_bin"
    utf8_general_ci = "utf8_general_ci"
    utf8_unicode_ci = "utf8_unicode_ci"
    utf8mb4_general_ci = "utf8mb4_general_ci"
    utf8mb4_unicode_ci = "utf8mb4_unicode_ci"
    
    latin1_bin = "latin1_bin"
    latin1_swedish_ci = "latin1_swedish_ci"
    latin1_general_ci = "latin1_general_ci"
    ascii_general_ci = "ascii_general_ci"
    latin2_general_ci = "latin2_general_ci"