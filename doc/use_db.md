# Use Methods

### In Mysql
```python
async def main():
    
    # Add multiple records
    await wallet.add_all((Wallet.user_id, Wallet.balance),[(1234, 10.0),(4321, 0)])
    
    # Add a record
    await transactions.add(wallet_id = 2, amount = 5.5, transactions_type = 1)
    
    # Update record
    await wallet.update(balance =  wallet.balance + 5.5).WHERE(wallet.wallet_id == 2).commit
    
    # Select record
    result = await wallet.select(wallet.user_id, Wallet.balance, wallet.created_at).WHERE(wallet.balance >= 5).ORDER_BY(wallet.balance,order="DESC").LIMIT(3).return_result
    print(result)
    
    # Delete record
    await transactions.delete().WHERE(transactions.amount == 0.0).commit
    

asyncio.get_event_loop().run_until_complete(main())
```


### In Sqlite
```python
async def main():
    
    # Add multiple records
    await wallet.add_all((Wallet.user_id, Wallet.balance, Wallet.created_at),[(1234, 10.0, str(datetime.now())),(4321, 0, str(datetime.now()))])
    
    # Add a record
    await transactions.add(wallet_id = 2, amount = 5.5, transactions_type = 1, transactions_date = str(datetime.now()))
    
    # Update record
    await wallet.update(balance =  wallet.balance + 5.5).WHERE(wallet.wallet_id == 2).commit
    
    # Select record
    result = await wallet.select(wallet.user_id, Wallet.balance, wallet.created_at).WHERE(wallet.balance >= 5).ORDER_BY(wallet.balance,order="DESC").LIMIT(3).return_result
    print(result)
    
    # Delete record
    await transactions.delete().WHERE(transactions.amount == 0.0).commit
    

asyncio.get_event_loop().run_until_complete(main())
```  
  
if you think you will forget to use `.commit`!  
you can use the following method:
```python
from sql1 import DELETE
```
```python
# useing .commit
await wallet.delete().WHERE(wallet.wallet_id == 1).commit

# without using .commit
await db.execute_commit(DELETE(wallet).WHERE(wallet.wallet_id == 1))
```     
These are just a few simple examples of this ORM!  
A large document will be presented to you soon.  
  
  
[< Back](start.md)

- [Install](install.md)
- [Creating table and cooneting the to Database](start.md)