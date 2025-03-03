# tinydb_interface.py
from tinydb import TinyDB, Query


class TinyDBInterface:
    """
    A simple, modular interface to TinyDB.

    Each instance creates its own TinyDB database and table.
    This makes it easy to create and use multiple instances concurrently.
    """

    def __init__(self, db_path='db.json', table_name='_default', **db_kwargs):
        """
        Initialize a new TinyDB instance.

        Args:
            db_path (str): Path to the TinyDB JSON file.
            table_name (str): Name of the table to use (default: '_default').
            db_kwargs: Additional keyword arguments to pass to TinyDB.
        """
        self.db = TinyDB(db_path, **db_kwargs)
        self.table = self.db.table(table_name)
        self._counter = 0  # Initialize internal counter

    def insert(self, element):
        """
        Insert an element (dict) into the table.

        Args:
            element (dict): The element to insert.

        Returns:
            int: The inserted element's ID.
        """
        return self.table.insert(element)

    def get_next_element(self):
        """
        Retrieve the next element from the table based on an internal counter.

        Returns:
            dict or None: The next element if available, or None if the table is empty.

        The counter is updated after each call and wraps around once it reaches the end.
        """
        all_elem = self.table.all()
        if not all_elem or self._counter >= len(all_elem):
            return None
        elem = all_elem[self._counter]
        self._counter += 1  # Update the counter for next call
        return elem

    def purge(self):
        """
        Remove all elements from the table.
        """
        self.table.truncate()

    def remove(self, condition):
        """
        Remove elements matching a condition.

        Args:
            condition: A TinyDB query condition.

        Returns:
            list: A list of IDs of the removed elements.
        """
        return self.table.remove(condition)


    def insert_multiple(self, elements):
        """
        Insert multiple elements.

        Args:
            elements (iterable): An iterable of element dictionaries.

        Returns:
            list: A list of inserted element IDs.
        """
        return self.table.insert_multiple(elements)

    def search(self, condition):
        """
        Search for elements matching a query condition.

        Args:
            condition: A TinyDB query condition (e.g. Query() or where(...)).

        Returns:
            list: A list of matching elements.
        """
        return self.table.search(condition)

    def update(self, fields, condition):
        """
        Update elements matching a condition.

        Args:
            fields (dict or callable): A dict with new values or a function that takes an element.
            condition: A TinyDB query condition.

        Returns:
            list: A list of IDs of the updated elements.
        """
        return self.table.update(fields, condition)


    def all(self):
        """
        Retrieve all elements in the table.

        Returns:
            list: A list of all elements.
        """
        return self.table.all()

    def close(self):
        """
        Close the underlying TinyDB instance.
        """
        self.db.close()