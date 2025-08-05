from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import sites
from .routers import llms

app = FastAPI(title="GEO SaaS API", version="0.1.0")

origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sites.router)
app.include_router(llms.router)

@app.get("/")
async def root():
    return {"status": "ok"}