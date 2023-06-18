import budgeting_app_backend.load_env  # noqa
from fastapi import FastAPI, UploadFile, HTTPException, Request
from typing import List
from budgeting_app_backend import (
    State,
    SpendingLimitsValue,
    CategoryExpansionsValue,
    AccountPropertiesValue,
    UploadDetailsValue,
    SqliteConnection,
    SqlSettings,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.openapi.utils import get_openapi
import os
import re


DB_URL = os.getenv("DB_URL")
TOKEN = os.getenv("TOKEN")
PASSWORD = os.getenv("PASSWORD")
BACKEND_URL = os.getenv("BACKEND_URL")
SQLITE_PATH = os.getenv("SQLITE_PATH")


app = FastAPI(docs_url="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_state() -> State:
    sqlite_connection = SqliteConnection(sqlite_path=SQLITE_PATH)
    app_settings = SqlSettings(sql_connection=sqlite_connection)
    return State(sql_connection=sqlite_connection, db_url=DB_URL, settings=app_settings)


def check_authorization(request: Request):
    authorization = request.headers.get("authorization")

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header not found")

    matches = re.match(r"^Bearer ([^ ]+)$", authorization)
    if not matches:
        raise HTTPException(
            status_code=401, detail='Authorization must be in format "Bearer TOKEN"'
        )

    token = matches[1]

    if token != TOKEN:
        raise HTTPException(status_code=400, detail="Not authenticated")


@app.get("/", tags=["System"])
async def root() -> str:
    return "OK"


@app.get("/config", tags=["System"])
async def config(password: str):
    if password != PASSWORD:
        raise HTTPException(status_code=400, detail="Not authenticated")

    return {"backend_token": TOKEN, "db_url": DB_URL}


@app.get("/settings", tags=["State"])
async def settings(request: Request) -> UploadDetailsValue:
    check_authorization(request)

    return create_state().settings()


@app.get("/transactions", tags=["State"])
async def transactions(request: Request) -> List:
    check_authorization(request)

    return create_state().transactions()


@app.post("/importing", tags=["State"])
async def importing(file: UploadFile, request: Request):
    check_authorization(request)

    content = file.file.read()
    create_state().importing(content)

    return "OK"


@app.get("/exporting", tags=["State"])
async def exporting(request: Request):
    check_authorization(request)

    csv_bytes = create_state().exporting()

    return StreamingResponse(
        iter([csv_bytes]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment;filename=export.csv"},
    )


@app.post("/dump", tags=["Debug"])
async def dump(request: Request):
    check_authorization(request)

    create_state().dump()

    return "OK"


@app.post("/spending-limits", tags=["State"])
async def set_spending_limits(value: SpendingLimitsValue, request: Request):
    check_authorization(request)

    create_state().set_spending_limits(value)

    return "OK"


@app.get("/spending-limits", tags=["State"])
async def get_spending_limits(request: Request) -> SpendingLimitsValue:
    check_authorization(request)

    return create_state().get_spending_limits()


@app.post("/category-expansions", tags=["State"])
async def set_category_expansion(value: CategoryExpansionsValue, request: Request):
    check_authorization(request)

    create_state().set_category_expansions(value)

    return "OK"


@app.get("/category-expansions", tags=["State"])
async def get_category_expansion(request: Request) -> CategoryExpansionsValue:
    check_authorization(request)

    return create_state().get_category_expansions()


@app.post("/account-properties", tags=["State"])
async def set_account_properties(value: AccountPropertiesValue, request: Request):
    check_authorization(request)

    create_state().set_account_properties(value)

    return "OK"


@app.get("/account-properties", tags=["State"])
async def get_account_properties(request: Request) -> AccountPropertiesValue:
    check_authorization(request)

    return create_state().get_account_properties()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Budgeting App API",
        version="0.1.0",
        description="Budgeting App API",
        routes=app.routes,
    )
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}
    openapi_schema["components"]["securitySchemes"]["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "TOKEN",
    }
    openapi_schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi
