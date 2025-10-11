import random

async def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

OTP_EXPIRY_MINUTES = 10
MAX_OTP_ATTEMPTS = 5
