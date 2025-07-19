from abc import ABC, abstractmethod
from functools import wraps

class BaseRepository(ABC):
    """
    Abstract base class for repositories, handling database dependency injection.
    """
    def __init__(self, db):
        """
        Initialize the repository with a database connection.

        Args:
            db (sqlite3.Connection): The database connection to use for this repository.
        """
        self.db = db

def with_repo_cls(repo_cls):
    """
    Decorator factory to inject a repository instance into the route handler.

    Args:
        repo_cls (type): The repository class to instantiate.

    Returns:
        callable: The decorator.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from main import get_db  # Local import to avoid circular imports
            db = get_db()
            repo = repo_cls(db)
            return f(repo, *args, **kwargs)
        return decorated_function
    return decorator 