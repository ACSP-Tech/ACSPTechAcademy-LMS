from decouple import config
from fastapi_mail import ConnectionConfig


DATABASE_URL = config('DATABASE_URL')

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
KEEP_ALIVE_TOKEN = config("KEEP_ALIVE_TOKEN")