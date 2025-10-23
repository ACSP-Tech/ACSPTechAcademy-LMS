#importing the necessary requirements
from fastapi import FastAPI
from .setup_main import configure_cors
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .database_setup import init_db
from contextlib import asynccontextmanager
from .setup_main import cleanup_otp
import asyncio
from fastapi_pagination import add_pagination


#import router
from .routers import keep_alive, root, register, verify, login, resend_email, logout, forgot_password, reset_password, verify_otp, user_profile, super_admin

#scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start-up code
    await init_db()
    otp_cleanup_task = asyncio.create_task(cleanup_otp())
    try:
        yield
    finally:
        otp_cleanup_task.cancel()
        try:
            await otp_cleanup_task
        except asyncio.CancelledError:
            pass



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
app.include_router(verify_otp.router)
app.include_router(user_profile.router)
app.include_router(super_admin.router)



#adding pagination to the app
add_pagination(app)