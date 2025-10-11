#importing the necessary requirements
from fastapi import FastAPI
from .setup_main import configure_cors
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .database_setup import init_db
from contextlib import asynccontextmanager


#import router
from .routers import keep_alive, root, register, verify, login, resend_email, logout, forgot_password, reset_password

#scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield



#calling an instance of fast api
app = FastAPI(
    title="E-Library API",
    description="API for managing an electronic library system",
    version="1.0.0",
    lifespan=lifespan
)

#definiing the cors function and any other custom middleware
configure_cors(app)


#include routers
app.include_router(keep_alive.router)
app.include_router(root.router)
app.include_router(register.router)
app.include_router(verify.router)
app.include_router(login.router)
app.include_router(resend_email.router)
app.include_router(logout.router)
app.include_router(forgot_password.router)
app.include_router(reset_password.router)