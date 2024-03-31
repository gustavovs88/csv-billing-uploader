from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import billing
from dependencies import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect db on app startup before starting to receive requests
    database.instance.connect()
    database.instance.create_tables()

    yield
    # Disconnect db on app shutdown after the last request
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
