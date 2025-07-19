FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only dependency files first for caching
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the app
COPY . .

EXPOSE 80

CMD ["poetry", "run", "python", "main.py", "--port", "80"] 