from fastapi import FastAPI
from typing import List
from dotenv import load_dotenv
from budgeting_app_backend.transactions import Example
from fastapi.middleware.cors import CORSMiddleware


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
    return Example().all()
