from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine,Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DB_URI = "postgresql://postgres:Sdreddy06@localhost:5432/postgres"
engine = create_engine(DB_URI)
local_session = sessionmaker(bind=engine,autocommit = False,autoflush = False)

Base = declarative_base()

class User(Base):
    __tablename__ = "newusers"
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String)
    age = Column(Integer)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
    
Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/getusers")
async def get_users(db:Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/user/{id}")
async def get_user(id:int,db:Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()

class UserDetails(BaseModel):
    name:str
    age:int


@app.post("/registerUser")
async def add_user(user:UserDetails, db:Session = Depends(get_db)):
    user_details = User(name = user.name,age = user.age)
    db.add(user_details)
    db.commit()
    return "added"

class UpdateUser(BaseModel):
    name:str = Field(default=None)
    age:int = Field(default=None)

@app.post("/updateUser/{id}")
async def updateUser(id:int,details:UpdateUser,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if details.name:
        user.name = details.name
    if details.age:
        user.age = details.age 
    
    db.commit()
    return "updated"