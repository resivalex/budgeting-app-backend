FROM python:3.11

WORKDIR /app

# Install project python dependencies
ADD ["pyproject.toml", "poetry.lock", "./"]
ENV PIP_NO_CONCURRENCY=1
RUN pip install --upgrade pip
RUN pip install poetry~=1.7.1 \
    && poetry config virtualenvs.in-project false \
    && poetry config virtualenvs.path /app/.venv-docker
RUN poetry install

ADD alembic alembic
ADD src src
RUN poetry install

ADD ["main.py", "pytest.ini", "alembic.ini", "./"]

CMD ["poetry", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
