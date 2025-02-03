from fastapi import FastAPI
from app.routers import router

import uvicorn
from app.database import create_tables

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    await create_tables()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
