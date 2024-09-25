from fastapi import FastAPI
import logging
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": os.getenv("DB_URI")}