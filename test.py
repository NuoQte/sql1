from mrdb import DataBase , Base , Column 
from mrdb.types import INT , DECIMAL , TIMESTAMP,CURRENT_TIMESTAMP
from datetime import datetime
import aiomysql
import asyncio


# Define Tabel
class Wallet(Base):
    __tablename__ = "wallet"
    wallet_id  = Column("wallet_id", INT,primary_key=True, auto_increment=True, index=True)
    user_id    = Column("user_id", INT, not_null=True)
    balance    = Column("balance", DECIMAL(10,2), not_null=True, default=0.0)
    created_at = Column("created_at", TIMESTAMP, default=CURRENT_TIMESTAMP)
    

wallet = Wallet()

class Transactions(Base):
    __tablename__ = "transactions"
    transactions_id   = Column("transactions_id", INT, primary_key=True, auto_increment=True, index=True)
    wallet_id         = Column("wallet_id", INT, foreign_key=wallet.wallet_id)
    amount            = Column("amount", DECIMAL(10,2), not_null=True)
    transactions_type = Column("transactions_type", INT)
    transactions_date = Column("transactions_date", TIMESTAMP, default=CURRENT_TIMESTAMP)
    
transactions = Transactions() 


# Create Database and Tabels

db = DataBase(aiomysql, database_name="db_test").create(wallet,transactions)

# Use Database
async def main():
    
    # Add multiple records
    await wallet.add_all({Wallet.user_id.str : 1234 ,Wallet.balance.str : 10.0},{Wallet.user_id.str : 4321})
    
    # Add a record
    await transactions.add(wallet_id = 2, amount = 5.5, transactions_type = 1)
    
    # Update record
    await wallet.update(wallet.balance ==  wallet.balance + 5.5).WHERE(wallet.id == 2).commit
    
    # Select record
    result = await wallet.select(wallet.user_id, Wallet.balance, wallet.created_at).WHERE(wallet.balance >= 5).ORDER_BY(wallet.created_at).return_result
    print(result)
    
    # Delete record
    await transactions.delete().WHERE(transactions.amount == 0.0)
    


asyncio.get_event_loop().run_until_complete(main())