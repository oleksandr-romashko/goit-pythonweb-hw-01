"""
Library Management System demonstrating SOLID principles.

This module defines a minimal console-based library system for managing books,
intended to showcase the application of SOLID design principles in Python.

Classes:
    - Book: Data container for book information.
    - AbstractStorage: Interface for storage operations.
    - LibraryStorage: In-memory implementation of AbstractStorage.
    - AbstractFormatter: Interface for formatting book output.
    - LibraryFormatter: Logs book information using logging.
    - LibraryInterface: Interface for library operations.
    - Library: Core library logic with injected storage and formatting.
    - LibraryManager: Command-line interface for user interaction.

Example:
    Run this module as a script to interact with the library system.
"""

# Note: This implementation deliberately omits production-level concerns such as:
#       - Data validation (e.g. checking if 'year' is an integer).
#       - Error handling (e.g. KeyboardInterrupt).
#       - User-facing messages (e.g. missing/duplicate book cases).
#       These aspects are intentionally excluded to focus on illustrating the SOLID
#       design principles clearly and concisely, without introducing unrelated complexity.
#
# Subtask 1: Follow SRP (Single Responsibility Principle):
#            - Separate Book class: encapsulates book data and formatting.
#            - LibraryStorage: manages book collection (add, remove, list).
#            - LibraryFormatter: handles book output formatting/logging.
#            - Library: delegates tasks and composes storage + formatter.
#            - LibraryManager: orchestrates CLI interaction with the library.
#
# Subtask 2: Follow OCP (Open/Closed Principle):
#            - Code promotes extensibility through abstraction and composition.
#            - Library and Formatter use abstract interfaces and are easily extendable
#              without modifying existing code (e.g., for new formats or storage types).
#            - New storage strategies (e.g., database, file) can be added without modifying
#              the Library class.
#            - String formatting of books is encapsulated in the Book class, making the system
#              open for formatting changes without modifying Library or Formatter.
#
# Subtask 3: Follow LSP (Liskov Substitution Principle):
#            - Library can be used interchangeably with its LibraryInterface type.
#
# Subtask 4: Follow ISP (Interface Segregation Principle):
#            - AbstractStorage and AbstractFormatter define minimal interfaces focused
#              on a single concern each. They are designed with narrow scopes, ensuring
#              classes only implement methods relevant to their purpose.
#
# Subtask 5: Follow DIP (Dependency Inversion Principle):
#            - LibraryManager (high-level module) depends only on LibraryInterface
#              (abstraction), not concrete implementations.


from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List
import logging

from goit_pythonweb_hw_01.utils.logging_config import setup_logging

logger = logging.getLogger("goit_pythonweb_hw_01.task_2")


@dataclass(frozen=True)
class Book:
    """Represents a book with a title, author, and publication year."""

    title: str
    author: str
    year: str

    def __str__(self) -> str:
        """Return a string representation of the book."""
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"


class AbstractStorage(ABC):
    """Interface for storing and managing a collection of items."""

    @abstractmethod
    def add_item(self, item: Any) -> None:
        """Add an item to storage."""
        pass

    @abstractmethod
    def remove_item_by_title(self, title: str) -> None:
        """Remove an item from storage by its title."""
        pass

    @abstractmethod
    def list_items(self) -> List[Any]:
        """Return a list of all stored items."""
        pass


class LibraryStorage(AbstractStorage):
    """In-memory implementation of AbstractStorage for Book items."""

    def __init__(self) -> None:
        """Initialize an empty book list."""
        self.items: List[Book] = []

    def add_item(self, item: Book) -> None:
        """Add a book to the storage if it doesn't already exist."""
        if item not in self.items:
            self.items.append(item)

    def remove_item_by_title(self, title: str) -> None:
        """Remove a book from the storage by its title."""
        self.items = [book for book in self.items if book.title != title]

    def list_items(self) -> List[Book]:
        """Return a copy of all stored books."""
        return self.items.copy()


class AbstractFormatter(ABC):
    """Interface for logging or displaying items."""

    @abstractmethod
    def log_items(self, items: List[Any]) -> None:
        """Log a list of items."""
        pass


class LibraryFormatter(AbstractFormatter):
    """Logs a list of Book objects using logging module."""

    def log_items(self, items: List[Book]) -> None:
        """Log each book in the list using the logger."""
        for book in items:
            logger.info("Book: %s", book)


class LibraryInterface(ABC):
    """Interface for basic library operations."""

    @abstractmethod
    def add_book(self, title: str, author: str, year: str) -> None:
        """Add a new book to the library."""
        pass

    @abstractmethod
    def remove_book(self, title: str) -> None:
        """Remove a book from the library by title."""
        pass

    @abstractmethod
    def show_books(self) -> None:
        """Display all books in the library."""
        pass


class Library(LibraryInterface):
    """Concrete implementation of a library using composition."""

    def __init__(
        self, book_storage: AbstractStorage, formatter: AbstractFormatter
    ) -> None:
        """
        Initialize the library with a storage and formatter implementation.

        Args:
            book_storage (AbstractStorage): The storage backend.
            formatter (AbstractFormatter): The output formatter.
        """
        self.book_storage = book_storage
        self.formatter = formatter

    def add_book(self, title: str, author: str, year: str) -> None:
        """Add a new book to the library."""
        book = Book(title, author, year)
        self.book_storage.add_item(book)

    def remove_book(self, title: str) -> None:
        """Remove a book from the library by title."""
        self.book_storage.remove_item_by_title(title)

    def show_books(self) -> None:
        """Display all books using the formatter."""
        books = self.book_storage.list_items()
        self.formatter.log_items(books)


class LibraryManager:
    """Command-line interface for interacting with the library."""

    def __init__(self, library: LibraryInterface):
        """
        Initialize the manager with a library interface.

        Args:
            library (LibraryInterface): The library to manage.
        """
        self.library = library

    def run(self) -> None:
        """Run the main command loop for user interaction."""

        while True:
            command = input("Enter command (add, remove, show, exit): ").strip().lower()

            match command:
                case "add":
                    title = input("Enter book title: ").strip()
                    author = input("Enter book author: ").strip()
                    year = input("Enter book year: ").strip()
                    self.library.add_book(title, author, year)
                case "remove":
                    title = input("Enter book title to remove: ").strip()
                    self.library.remove_book(title)
                case "show":
                    self.library.show_books()
                case "exit":
                    break
                case _:
                    print("Invalid command. Please try again.")


def main() -> None:
    """Entry point for running the library management system."""
    setup_logging()

    storage = LibraryStorage()
    formatter = LibraryFormatter()
    library: LibraryInterface = Library(storage, formatter)
    library_manager = LibraryManager(library)

    library_manager.run()


if __name__ == "__main__":
    main()
