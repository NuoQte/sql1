# Creating table and cooneting the to Database

### Create Tabels in Mysql
```python
from mrdb import DataBase , Base , Column 
from mrdb.types import INT , DECIMAL , TIMESTAMP,CURRENT_TIMESTAMP
import aiomysql , asyncio


# Define Tabel
class Wallet(Base):
    _tablename_ = "wallet"
    wallet_id  = Column("wallet_id", INT,primary_key=True, auto_increment=True, index=True)
    user_id    = Column("user_id", INT, not_null=True)
    balance    = Column("balance", DECIMAL(10,2), not_null=True, default=0.0)
    created_at = Column("created_at", TIMESTAMP, default=CURRENT_TIMESTAMP)
    
wallet = Wallet()


class Transactions(Base):
    _tablename_ = "transactions"
    transactions_id   = Column("transactions_id", INT, primary_key=True, auto_increment=True, index=True)
    wallet_id         = Column("wallet_id", INT, foreign_key=wallet.wallet_id)
    amount            = Column("amount", DECIMAL(10,2), not_null=True)
    transactions_type = Column("transactions_type", INT)
    transactions_date = Column("transactions_date", TIMESTAMP, default=CURRENT_TIMESTAMP)
    
transactions = Transactions() 


# Create Database and Tabels
db = DataBase(aiomysql, database_name="db_test").create(wallet,transactions)
```

### Create Tabels in Sqlite
```python
from mrdb import DataBase , Base , Column 
from mrdb.types import INTEGER , REAL , TEXT
from datetime import datetime
import aiosqlite , asyncio


# Define Tabel
class Wallet(Base):
    _tablename_ = "wallet"
    wallet_id  = Column("wallet_id", INTEGER,primary_key=True, autoincrement=True)
    user_id    = Column("user_id", INTEGER, not_null=True)
    balance    = Column("balance", REAL, not_null=True, default=0.0)
    created_at = Column("created_at", TEXT,)
    

wallet = Wallet()

class Transactions(Base):
    _tablename_ = "transactions"
    transactions_id   = Column("transactions_id", INTEGER, primary_key=True, autoincrement=True)
    wallet_id         = Column("wallet_id", INTEGER, foreign_key=wallet.wallet_id)
    amount            = Column("amount", REAL, not_null=True)
    transactions_type = Column("transactions_type", INTEGER)
    transactions_date = Column("transactions_date", TEXT)
    
transactions = Transactions() 


# Create Database and Tabels
db = DataBase(aiosqlite, database_name="db_test").create(wallet,transactions)
```

[< Back](install.md) | [Next >](use_db.md)

- [Install](install.md)
- [Use Methods](use_db.md)