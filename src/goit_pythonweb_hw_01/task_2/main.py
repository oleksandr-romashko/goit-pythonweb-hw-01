from abc import ABC, abstractmethod
from typing import Any, List
from dataclasses import dataclass
import logging

from goit_pythonweb_hw_01.utils.logging_config import setup_logging

logger = logging.getLogger("goit_pythonweb_hw_01.task_2")


# TODO: 1. Щоб виконати принцип єдиної відповідальності (SRP), створіть клас Book, який відповідатиме за зберігання інформації про книгу.
# TODO: 2. Щоб забезпечити принцип відкритості/закритості (OCP), зробіть так, щоб клас Library міг бути розширений для нової функціональності без зміни його коду.
# TODO: 3. Щоб виконати принцип підстанови Лісков (LSP), переконайтеся, що будь-який клас, який наслідує інтерфейс LibraryInterface, може замінити клас Library без порушення роботи програми.
# TODO: 4. Щоб виконати принцип розділення інтерфейсів (ISP), використовуйте інтерфейс LibraryInterface для чіткої специфікації методів, які необхідні для роботи з бібліотекою library.
# TODO: 5. Щоб виконати принцип інверсії залежностей (DIP), зробіть так, щоб класи вищого рівня, такі як LibraryManager, залежали від абстракцій (інтерфейсів), а не від конкретних реалізацій класів.


# Note: Data validation (e.g. int parse for year), additional messages, KeyboardInterrupt error
#       handling, etc. are deliberately omitted in this task as this task focuses solely on SOLID
#       principles and such additional implementation (which are usual part of regular production code)
#       will bring additional out of scope noise to the code.
#
# Subtask 1: Follows SRP (Single Responsibility Principle):
#            - Each class has a clear, single responsibility:
#                - Book: encapsulates book data and string representation.
#                - LibraryStorage: manages book collection (add, remove, list).
#                - LibraryFormatter: responsible for formatting/logging book output.
#                - Library: coordinates operations using composition, delegates tasks.
#            - Responsibilities are well-separated, promoting maintainability and clarity.
# Subtask 2: Follows OCP (Open/Closed Principle):
#            - Library depends on abstract types (AbstractLibraryStorage), not concrete ones.
#            - New storage strategies (e.g., database, file) can be added without modifying the Library class.
#            - Formatter can be extended (e.g., JSONFormatter) without changing core logic.
#            - String formatting of books is encapsulated in the Book class, making the system
#              open for formatting changes without modifying Library or Formatter.
#            - Promotes extensibility through abstraction and composition.
# Subtask 3: Follows LSP (Liskov Substitution Principle):
#            - By inheriting from AbstractLibrary, the Library class guarantees that it can be
#              substituted wherever the AbstractLibrary interface is expected without breaking
#              the program's logic.


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    year: str

    def __str__(self) -> str:
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"


class AbstractStorage(ABC):
    @abstractmethod
    def add_item(self, item: Any) -> None:
        pass

    @abstractmethod
    def remove_item_by_title(self, title: str) -> None:
        pass

    @abstractmethod
    def list_items(self) -> List[Any]:
        pass


class LibraryStorage(AbstractStorage):
    def __init__(self) -> None:
        self.items: List[Book] = []

    def add_item(self, item: Book) -> None:
        if item not in self.items:
            self.items.append(item)

    def remove_item_by_title(self, title: str) -> None:
        self.items = [book for book in self.items if book.title != title]

    def list_items(self) -> List[Book]:
        return self.items.copy()


class AbstractFormatter(ABC):
    @abstractmethod
    def log_items(self, items: List[Any]) -> None:
        pass


class LibraryFormatter(AbstractFormatter):
    def log_items(self, items: List[Book]) -> None:
        for book in items:
            logger.info("Book: %s", book)


class AbstractLibrary(ABC):
    @abstractmethod
    def add_book(self, title: str, author: str, year: str) -> None:
        pass

    @abstractmethod
    def remove_book(self, title: str) -> None:
        pass

    @abstractmethod
    def show_books(self) -> None:
        pass


class Library(AbstractLibrary):
    def __init__(self) -> None:
        self.book_storage: AbstractStorage = LibraryStorage()
        self.formatter: AbstractFormatter = LibraryFormatter()

    def add_book(self, title: str, author: str, year: str) -> None:
        book = Book(title, author, year)
        self.book_storage.add_item(book)

    def remove_book(self, title: str) -> None:
        self.book_storage.remove_item_by_title(title)

    def show_books(self) -> None:
        books = self.book_storage.list_items()
        self.formatter.log_items(books)


def main() -> None:
    """Run example usage of the Library Managements System."""
    setup_logging()

    library: AbstractLibrary = Library()

    while True:
        command = input("Enter command (add, remove, show, exit): ").strip().lower()

        match command:
            case "add":
                title = input("Enter book title: ").strip()
                author = input("Enter book author: ").strip()
                year = input("Enter book year: ").strip()
                library.add_book(title, author, year)
            case "remove":
                title = input("Enter book title to remove: ").strip()
                library.remove_book(title)
            case "show":
                library.show_books()
            case "exit":
                break
            case _:
                print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
