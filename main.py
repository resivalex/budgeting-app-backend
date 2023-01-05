from fastapi import FastAPI
from typing import List
from dotenv import load_dotenv
from budgeting_app_backend.transactions import Example


load_dotenv()


app = FastAPI(docs_url='/api')


@app.get('/', tags=['System'])
async def root() -> str:
    return 'OK'


@app.get('/transactions', tags=['State'])
async def transactions() -> List:
    return Example().all()
