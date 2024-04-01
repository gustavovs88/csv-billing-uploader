import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import billing
from dependencies import database
from services.billing import issue_receipts_cron_job
from services.scheduler import run_scheduler

shutdown_event = asyncio.Event()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect db on app startup before starting to receive requests
    database.instance.connect()
    database.instance.create_tables()
    # issue_receipts_cron_job()
    from services.scheduler import run_scheduler

    asyncio.create_task(run_scheduler())

    yield

    # Disconnect db on app shutdown after the last request
    async def shutdown_event():
        shutdown_event.set()

    database.instance.disconnect()


app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost:8888",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(billing.router)


@app.get("/")
async def root():
    return {"message": "Hello Kanastra, this is Gustavo's project."}
