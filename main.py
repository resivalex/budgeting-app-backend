import budgeting_app_backend.load_env # noqa
from fastapi import FastAPI, UploadFile, HTTPException
from typing import List
from budgeting_app_backend import (
    State,
    CurrencyConfigValue,
    SpendingLimitsValue,
    CategoryExpansionsValue,
    SqliteConnection,
    Settings
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os


DB_URL = os.getenv('DB_URL')
TOKEN = os.getenv('TOKEN')
PASSWORD = os.getenv('PASSWORD')
BACKEND_URL = os.getenv('BACKEND_URL')
SQLITE_PATH = os.getenv('SQLITE_PATH')


app = FastAPI(docs_url='/api')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def validate_token(token: str = None):
    if token != TOKEN:
        raise HTTPException(status_code=400, detail='Not authenticated')


def create_state() -> State:
    sqlite_connection = SqliteConnection(sqlite_path=SQLITE_PATH)
    app_settings = Settings(sql_connection=sqlite_connection)
    return State(sql_connection=sqlite_connection, db_url=DB_URL, settings=app_settings)


@app.get('/', tags=['System'])
async def root() -> str:
    return 'OK'


@app.get('/config', tags=['System'])
async def config(password: str):
    if password != PASSWORD:
        raise HTTPException(status_code=400, detail='Not authenticated')

    return {
        'backend_token': TOKEN,
        'db_url': DB_URL
    }


@app.get('/settings', tags=['State'])
async def settings(token: str) -> dict:
    validate_token(token)

    return create_state().settings()


@app.get('/transactions', tags=['State'])
async def transactions(token: str) -> List:
    validate_token(token)

    return create_state().transactions()


@app.post('/importing', tags=['State'])
async def importing(file: UploadFile, token: str):
    validate_token(token)

    content = file.file.read()
    create_state().importing(content)

    return 'OK'


@app.get('/exporting', tags=['State'])
async def exporting(token: str):
    validate_token(token)

    csv_bytes = create_state().exporting()

    return StreamingResponse(
        iter([csv_bytes]),
        media_type='text/csv',
        headers={
            'Content-Disposition': 'attachment;filename=export.csv'
        }
    )


@app.post('/dump', tags=['Debug'])
async def dump(token: str):
    validate_token(token)

    create_state().dump()

    return 'OK'


@app.post('/currency_config', tags=['State'])
async def set_currency_config(value: CurrencyConfigValue, token: str):
    validate_token(token)

    create_state().set_currency_config(value)

    return 'OK'


@app.get('/currency_config', tags=['State'])
async def get_currency_config(token: str) -> CurrencyConfigValue:
    validate_token(token)

    return create_state().get_currency_config()


@app.post('/spending_limits', tags=['State'])
async def set_spending_limits(value: SpendingLimitsValue, token: str):
    validate_token(token)

    create_state().set_spending_limits(value)

    return 'OK'


@app.get('/spending_limits', tags=['State'])
async def get_spending_limits(token: str) -> SpendingLimitsValue:
    validate_token(token)

    return create_state().get_spending_limits()


@app.post('/category_expansions', tags=['State'])
async def set_category_expansion(value: CategoryExpansionsValue, token: str):
    validate_token(token)

    create_state().set_category_expansions(value)

    return 'OK'


@app.get('/category_expansions', tags=['State'])
async def get_category_expansion(token: str) -> CategoryExpansionsValue:
    validate_token(token)

    return create_state().get_category_expansions()
