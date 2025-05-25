from models import Account
from passlib import bcrypt

async def create_user(name, lastname, email, password:str, role=None):
    h = bcrypt.hash(password)
    await Account.create(
        email=email,
        name=name,lastname=lastname, password=h,role=role
    )

# async def 

async def verify_password(email, password):
    a = await Account.get(email=email)
    if not a:
        raise ValueError(f"No Account with email={email} found.")
    
    if a.password == bcrypt.hash(password):
        return True
    return False
