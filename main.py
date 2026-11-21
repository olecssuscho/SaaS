import logging
from fastapi import FastAPI
from routers import users
from lim import limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from fastapi_pagination import add_pagination

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

app = FastAPI()

app.include_router(users.router)

add_pagination(app)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
def root():
    return {"Message":"Hello"}

