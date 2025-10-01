from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], depreciated="auto")

async def password_hash(password):
    "permently Hash plain password"
    return await pwd_context.hash(password)