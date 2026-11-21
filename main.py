import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

app = FastAPI()

@app.get("/")
def root():
    return {"Message":"Hello"}

