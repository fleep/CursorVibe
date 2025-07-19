FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only dependency files first for caching
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the app
COPY . .

EXPOSE 8080

CMD ["poetry", "run", "python", "main.py", "--host", "0.0.0.0", "--port", "8080"] 