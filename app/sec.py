from decouple import config
from fastapi_mail import ConnectionConfig


DATABASE_URL = config('DATABASE_URL')

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
KEEP_ALIVE_TOKEN = config("KEEP_ALIVE_TOKEN")

conf = ConnectionConfig(
MAIL_USERNAME=config('MAIL_USERNAME'),
MAIL_PASSWORD = config('MAIL_PASSWORD'),
MAIL_FROM = config('MAIL_FROM'),
MAIL_PORT = int(config('MAIL_PORT')),
MAIL_SERVER = config('MAIL_SERVER'),
MAIL_TLS = True,
MAIL_SSL = False
)
