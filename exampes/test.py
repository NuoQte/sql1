from msm import DataBase , Base , Column
from msm.types import INT , VARCHAR


# Def table
class Users(Base):
    __tablename__ = 'users'
    id = Column('id',INT,primary_key=True,auto_increment=True,index=True)
    name = Column('name',VARCHAR(50),not_null=True)
    username = Column('username',VARCHAR(30))
    

# tabel obj
user = Users()

# connect 
db = DataBase(database_name='testlib').create(user)
