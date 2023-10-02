from fastapi import FastAPI

from src.auth.base_config import auth_backend, fastapi_users

from src.auth.shemas import UserRead, UserCreate
from src.operations.router import router as router_operation
app = FastAPI(title='Test API')



app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


app.include_router(router_operation)