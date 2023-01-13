from fastapi import FastAPI, UploadFile
from typing import List
from dotenv import load_dotenv
from budgeting_app_backend import DbSource, CsvImporting
from fastapi.middleware.cors import CORSMiddleware
import os


load_dotenv()


app = FastAPI(docs_url='/api')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', tags=['System'])
async def root() -> str:
    return 'OK'


@app.get('/transactions', tags=['State'])
async def transactions() -> List:
    return DbSource(
        url=os.getenv('DB_URL'),
        name=os.getenv('DB_NAME')
    ).all()


@app.post('/importing', tags=['State'])
async def importing(file: UploadFile):
    content = file.file.read()
    importing = CsvImporting(
        url=os.getenv('DB_URL'),
        name=os.getenv('DB_NAME')
    )

    importing.perform(content)

    return 'OK'
