FROM python:3.9

WORKDIR /app

# Install project python dependencies
ADD ["pyproject.toml", "poetry.lock", "./"]
RUN pip install poetry~=1.3.1 \
    && poetry config virtualenvs.in-project false \
    && poetry config virtualenvs.path /app/.venv-docker
RUN poetry install

ADD src src
RUN poetry install

ADD ["main.py", "pytest.ini", "./"]

CMD ["poetry", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
