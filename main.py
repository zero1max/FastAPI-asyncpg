from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="User",
    version='0.0.1',
    description="FastAPI CRUD Asyncpg",
    debug=True,
)

app.include_router(router)  # Routerni to'g'ri qo'shamiz

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
