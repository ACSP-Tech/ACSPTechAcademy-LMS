from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def password_hash(password):
    "permently Hash plain password"
    return pwd_context.hash(password)