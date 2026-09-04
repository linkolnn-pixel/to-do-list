from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router
from app.core.logging import configure_logging
from app.middleware.request_logger import log_request

configure_logging()
app = FastAPI()
app.include_router(router=task_router)
app.include_router(router=category_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.middleware("http")(log_request)









