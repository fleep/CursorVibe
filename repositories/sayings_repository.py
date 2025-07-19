from typing import List, Dict, Any, Optional
from .base_repository import BaseRepository

class SayingsRepository(BaseRepository):
    """
    Repository for CRUD operations on the sayings table.
    """
    def get_all_sayings(self) -> List[Dict[str, Any]]:
        """
        Return all sayings from the database, ordered by creation timestamp descending.

        Returns:
            List[Dict[str, Any]]: A list of all sayings as dictionaries.
        """
        cur = self.db.execute('SELECT * FROM sayings ORDER BY ts_created DESC')
        return [dict(row) for row in cur.fetchall()]

    def get_saying_by_id(self, saying_id: int) -> Optional[Dict[str, Any]]:
        """
        Return a single saying by its ID, or None if not found.

        Args:
            saying_id (int): The ID of the saying to retrieve.

        Returns:
            Optional[Dict[str, Any]]: The saying as a dictionary, or None if not found.
        """
        cur = self.db.execute('SELECT * FROM sayings WHERE id = ?', (saying_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def add_saying(self, saying_id: int, summary: str, description: str, ts_created: str) -> None:
        """
        Insert a new saying into the database.

        Args:
            saying_id (int): The ID for the new saying.
            summary (str): The summary text of the saying.
            description (str): The description of the saying.
            ts_created (str): The creation timestamp (ISO format).

        Returns:
            None
        """
        with self.db:
            self.db.execute(
                'INSERT INTO sayings (id, summary, description, ts_created) VALUES (?, ?, ?, ?)',
                (saying_id, summary, description, ts_created)
            )

    def delete_saying(self, saying_id: int) -> int:
        """
        Delete a saying by its ID. Returns the number of rows deleted (0 or 1).

        Args:
            saying_id (int): The ID of the saying to delete.

        Returns:
            int: The number of rows deleted (0 if not found, 1 if deleted).
        """
        with self.db:
            cur = self.db.execute('DELETE FROM sayings WHERE id = ?', (saying_id,))
            return cur.rowcount

    def update_saying(self, saying_id: int, summary: str, description: str) -> None:
        """
        Update the summary and description of a saying by its ID.

        Args:
            saying_id (int): The ID of the saying to update.
            summary (str): The new summary text.
            description (str): The new description text.

        Returns:
            None
        """
        with self.db:
            self.db.execute(
                'UPDATE sayings SET summary = ?, description = ? WHERE id = ?',
                (summary, description, saying_id)
            )

    def id_exists(self, saying_id: int) -> bool:
        """
        Check if a saying with the given ID exists in the database.

        Args:
            saying_id (int): The ID to check for existence.

        Returns:
            bool: True if the ID exists, False otherwise.
        """
        cur = self.db.execute('SELECT 1 FROM sayings WHERE id = ?', (saying_id,))
        return cur.fetchone() is not None 