from app.sec import SECRET_KEY, ALGORITHM
import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta

async def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Please log in again.",
        )
    
async def encode_token(payload, expires_delta: int = 720):
    """
    Encode a JWT token with the given payload and expiration time.
    Args:
        payload (dict): The data to encode in the token.
        expires_delta (int, optional): Expiration time in minutes. Default is 120 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expires_delta)

    # Add issued-at and expiry
    to_encode.update({
        "iat": now,
        "exp": expire
    })

    # return encoded JWT token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def encode_email_token(payload, expires_delta: int = 1440):
    """
    Encode a JWT token with the given payload and expiration time.
    Args:
        payload (dict): The data to encode in the token.
        expires_delta (int, optional): Expiration time in minutes. Default is 120 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expires_delta)

    # Add issued-at and expiry
    to_encode.update({
        "iat": now,
        "exp": expire
    })

    # return encoded JWT token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

