import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes import products, users
from app.database import engine, Base
from app.exceptions import DuplicateSKUError, ProductNotFoundError, DuplicateUserError
from app.core.logging_config import setup_logging
from app.core.request_context import set_request_id


setup_logging()

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(products.router)
app.include_router(users.router)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    set_request_id(request_id)
    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/", include_in_schema=False)
def read_root():
    return {"Message": "Inventory Manager API is up and running!"}


@app.get("/health", include_in_schema=False)
def health():
    return {"Status": "OK"}


@app.get("/async-test", include_in_schema=False)
def async_test():
    return {"Message": "Async endpoint"}


@app.exception_handler(DuplicateSKUError)
async def duplicate_sku_handler(request: Request, exc: DuplicateSKUError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(DuplicateUserError)
async def duplicate_user_handler(request: Request, exc: DuplicateUserError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"detail": "Something went wrong, is not you it's us"}
    )
