FROM python:3.9

WORKDIR /app

# Install project python dependencies
ADD ["pyproject.toml", "poetry.lock", "./"]
RUN pip install --upgrade pip
RUN curl -sSL https://install.python-poetry.org | python -
RUN poetry config virtualenvs.in-project false \
    && poetry config virtualenvs.path /app/.venv-docker
RUN poetry install

ADD alembic alembic
ADD src src
RUN poetry install

ADD ["main.py", "pytest.ini", "alembic.ini", "./"]

CMD ["poetry", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
