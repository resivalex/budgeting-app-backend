from fastapi import FastAPI, UploadFile, HTTPException
from typing import List
from dotenv import load_dotenv
from budgeting_app_backend import DbSource, CsvImporting
from fastapi.middleware.cors import CORSMiddleware
import os


load_dotenv()


DB_URL = os.getenv('DB_URL')
TOKEN = os.getenv('TOKEN')


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


@app.get('/', tags=['System'])
async def root() -> str:
    return 'OK'


@app.get('/transactions', tags=['State'])
async def transactions(token: str) -> List:
    validate_token(token)

    return DbSource(url=DB_URL).all()


@app.post('/importing', tags=['State'])
async def importing(file: UploadFile, token: str):
    validate_token(token)

    content = file.file.read()
    csv_importing = CsvImporting(url=DB_URL)

    csv_importing.perform(content)

    return 'OK'
