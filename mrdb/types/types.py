from types import SimpleNamespace
import json

class RCD(SimpleNamespace):
    def __repr__(self):
        return json.dumps(self.__dict__,indent=4)



class BaseType:
    
    __pr__ = ''
    __su__ = ''
    
    def __init__(self,string="",pr="",su=""):
        self.__string__= f"{string}"
        self.__pr__ = pr
        self.__su__ = su
    
    def __str__(self):
        return self.__string__
    
    def __repr__(self):
        return self.__string__
    
    
    def __eq__(self, value):
        self.__string__+= f' = {self.__pr__}{value}{self.__su__}'
        return self

    def __ne__(self, value):
        self.__string__+= f' != {self.__pr__}{value}{self.__su__}'
        return self
    
    def  __gt__(self,value):
        self.__string__+= f' > {self.__pr__}{value}{self.__su__}'
        return self
    def __lt__(self,value):
        self.__string__+= f' < {self.__pr__}{value}{self.__su__}'
        return self
    def  __ge__(self,value):
        self.__string__+= f' >= {self.__pr__}{value}{self.__su__}'
        return self
    def __le__(self,value):
        self.__string__+= f' <= {self.__pr__}{value}{self.__su__}'
        return self
    def __or__(self, value):
        self.__string__+= f' OR {self.__pr__}{value}{self.__su__}'
        return self
    def __and__(self,value):
        self.__string__+= f' AND {self.__pr__}{value}{self.__su__}'
        return self
    def __add__(self, value):
        self.__string__+= f' + {self.__pr__}{value}{self.__su__}'
        return self
    def __sub__(self, value):
        self.__string__+= f' - {self.__pr__}{value}{self.__su__}'
        return self
    def __mul__(self, value):
        self.__string__+= f' * {self.__pr__}{value}{self.__su__}'
        return self

    def __truediv__(self, value):
        self.__string__+= f' / {self.__pr__}{value}{self.__su__}'
        return self
                
    def __floordiv__(self, value):
        self.__string__+= f' // {self.__pr__}{value}{self.__su__}'
        return self
    def __mod__(self, value):
        self.__string__+= f' % {self.__pr__}{value}{self.__su__}'
        return self
    def __pow__(self, value):
        self.__string__+= f' ** {self.__pr__}{value}{self.__su__}'
        return self

    
    def __contains__(self,value):
        self.__string__+= f' {value} IN {self.__string__}' 
        return self


class DataType:
    __pr__ = ""
    __su__ = ""
    TYPE :str = None
    
    def __str__(self):
        return self.TYPE
    def __repr__(self):
        return self.TYPE



class VARCHAR(DataType):
    __pr__ = "'"
    __su__ = "'"
    def __init__(self,n):
        self.TYPE = f'VARCHAR({n})'

class CHAR(DataType):
    __pr__ = "'"
    __su__ = "'"
    def __init__(self,n):
        self.TYPE = f'CHAR({n})'

class TEXT(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "TEXT"

class TINYTEXT(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "TINYTEXT"

class MEDIUMTEXT(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "MEDIUMTEXT"

class LONGTEXT(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "LONGTEXT"

class BLOB(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "BLOB"

class TINYBLOB(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "TINYBLOB"

class MEDIUMBLOB(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "MEDIUMBLOB"

class LONGBLOB(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "LONGBLOB"

class BINARY(DataType):
    __pr__ = "'"
    __su__ = "'"
    def __init__(self,v):
        self.TYPE = f"BINARY({v})"
    
class VARBINARY(DataType):
    __pr__ = "'"
    __su__ = "'"
    def __init__(self,v):
        self.TYPE = f"VARBINARY({v})"


class DATE(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "DATE"

class DATETIME(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "DATETIME"


class TIME(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "TIME"


class TIMESTAMP(DataType):
    __pr__ = "'"
    __su__ = "'"
    TYPE = "TIMESTAMP"

# class CURRENT_TIMESTAMP(DataType):
#     __pr__ = "'"
#     __su__ = "'"
#     TYPE = "CURRENT_TIMESTAMP"

CURRENT_TIMESTAMP = "CURRENT_TIMESTAMP"

class YEAR(DataType):
    __pr__ = "'"
    __su__ = "'"
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
    __pr__ = "'"
    __su__ = "'"
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