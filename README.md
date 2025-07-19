# CursorVibe

A Flask web server with a REST API for sayings, using SQLite (no ORM), Bootstrap 5, and Poetry for dependency management.

## Features
- Homepage rendered with Jinja2 and styled with Bootstrap 5 (CDN) + custom CSS
- REST API for a "saying" resource (CRUD)
- SQLite database (no ORM)
- Poetry for dependency management

## Setup

1. **Install dependencies:**
   ```sh
   poetry install
   ```

2. **Run the server:**
   ```sh
   poetry run python app.py
   ```

3. **Access the app:**
   - Homepage: [http://localhost:5000/](http://localhost:5000/)
   - API: [http://localhost:5000/sayings](http://localhost:5000/sayings)

## Project Structure
```
app.py
static/
    global.css
templates/
    index.html
pyproject.toml
README.md
```

## API Endpoints
- `GET /sayings` — List all sayings
- `GET /saying/<id>` — Get a saying by ID
- `POST /sayings` — Add a new saying (JSON: summary, description)
- `DELETE /saying/<id>` — Delete a saying by ID
- `PATCH /saying/<id>` — Update a saying by ID (JSON: summary, description)

## Notes
- All custom CSS should go in `static/global.css`.
- The database is created automatically on first run. 