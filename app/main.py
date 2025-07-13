from fastapi import FastAPI
from app.api import (
    auth_router,
    decrypt_qr_router,
    users_router,
    log_same_day_router,
    log_leave_router,
)

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(decrypt_qr_router.router)
app.include_router(users_router.router)
app.include_router(log_same_day_router.router)
app.include_router(log_leave_router.router)
