from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def password_hash(password):
    """permently Hash plain password"""
    return pwd_context.hash(password)

async def password_verify(plain_password, hashpassword):
    """verify user password"""
    return pwd_context.verify(plain_password, hashpassword)