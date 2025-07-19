import os
import sqlite3
from flask import Flask, g
from frontend import frontend_bp
from api.sayings import sayings_bp
from datetime import datetime
import random

app = Flask(__name__)

app.register_blueprint(frontend_bp)
app.register_blueprint(sayings_bp)

DATABASE = 'sayings.db'

# --- Database helpers ---
def get_db():
    """
    Get a SQLite database connection for the current app context, with row factory set to dict-like access.

    Returns:
        sqlite3.Connection: The SQLite database connection for the current app context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    """
    Initialize the database and create the sayings table if it does not exist. Insert initial records if the table is empty.

    Returns:
        None
    """
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS sayings (
                id INTEGER PRIMARY KEY,
                summary TEXT NOT NULL,
                description TEXT,
                ts_created TEXT NOT NULL
            )
        ''')
        db.commit()
        # Insert initial records if table is empty
        cur = db.execute('SELECT COUNT(*) as count FROM sayings')
        count = cur.fetchone()['count']
        if count == 0:
            now = datetime.utcnow().isoformat()
            initial_sayings = [
                {
                    'summary': 'The early bird catches the worm.',
                    'description': 'Success comes to those who prepare well and put in effort early.',
                },
                {
                    'summary': 'A stitch in time saves nine.',
                    'description': 'Dealing with a problem promptly will prevent it from getting worse.',
                },
                {
                    'summary': 'Actions speak louder than words.',
                    'description': 'What people do is more important than what they say.',
                },
            ]
            for saying in initial_sayings:
                saying_id = random.randint(100000, 999999)
                db.execute(
                    'INSERT INTO sayings (id, summary, description, ts_created) VALUES (?, ?, ?, ?)',
                    (saying_id, saying['summary'], saying['description'], now)
                )
            db.commit()

@app.teardown_appcontext
def close_connection(exception):
    """
    Close the database connection at the end of the app context.

    Args:
        exception (Exception): The exception that caused the teardown, if any.

    Returns:
        None
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    """
    Run the Flask development server after initializing the database.

    Returns:
        None
    """
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True) 
    