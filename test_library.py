import unittest
import os
import csv
from library import LibraryInventoryManager
from db_manager import DBManager
from datetime import datetime

"""
Program: LibraryInventoryManager
File: test_library.py
Author: Danielle Ihm
Last date modified: 12/06/2024
Course: CIS189
IDE: PyCharm
Academic Honesty: I attest that this is my original work.
I have not used unauthorized source code, either modified or unmodified.       
Resources Used:
    “CSV - Csv File Reading and Writing.” Python Documentation, docs.python.org/3/library/csv.html. Accessed 15 Nov. 2024.
    DMACC, CIS189 M13 T2: Connecting to a Database Demonstration Video, provided by Professor Jonathan Buys.
    “Datetime - Basic Date and Time Types.” Python Documentation, docs.python.org/3/library/datetime.html. Accessed 23 Nov. 2024.
    “Graphical User Interfaces with TK.” Python Documentation, docs.python.org/3/library/tk.html. Accessed 29 Nov. 2024.
"""

class TestLibraryInventoryManager(unittest.TestCase):

    def setUp(self):
        # Make a separate test inventory file for testing
        self.test_inventory_file = "test_inventory.csv"

        # Initialize in-memory list to simulate database
        self.db_manager = DBManager(self.test_inventory_file)
        self.inventory_manager = LibraryInventoryManager(self.db_manager, inventory_file=self.test_inventory_file)

        # Initialize with sample book data for testing
        self.db_manager.books = [
            {'title': 'Hatchet', 'author': 'Gary Paulsen', 'isbn': '1416936475', 'quantity': 5, 'checked_out_by_first_name': '', 'checked_out_by_last_name': ''},
            {'title': 'The Magician\'s Elephant', 'author': 'Kate DiCamillo', 'isbn': '0763680885', 'quantity': 3, 'checked_out_by_first_name': '', 'checked_out_by_last_name': ''},
            {'title': 'The Miraculous Journey of Edward Tulane', 'author': 'Kate DiCamillo', 'isbn': '076364821X', 'quantity': 2, 'checked_out_by_first_name': '', 'checked_out_by_last_name': ''}
        ]

        # Create a new test CSV file and write initial data
        with open(self.test_inventory_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'author', 'isbn', 'quantity', 'checked_out_by_first_name', 'checked_out_by_last_name']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in self.db_manager.books:
                writer.writerow(book)

    # Clean up: Delete test inventory file after each test
    def tearDown(self):
        if os.path.exists(self.test_inventory_file):
            os.remove(self.test_inventory_file)

        # Test search for "adventure" (no matching books)
        result = self.inventory_manager.search_books("adventure")
        self.assertEqual(len(result), 0)

        # Add book
    def test_check_out_book(self):
        book = {'title': 'Hatchet', 'author': 'Gary Paulsen', 'isbn': '1416936475', 'quantity': 3, 'checked_out_by_first_name': '', 'checked_out_by_last_name': ''}
        self.db_manager.books = [book]

        # Check out book
        self.inventory_manager.check_out_book(book, 'Roald', 'Dahl')

        # Check quantity is reduced by 1
        self.assertEqual(book['quantity'], 2)

        # Check student info is stored correctly
        self.assertEqual(book['checked_out_by_first_name'], 'Roald')
        self.assertEqual(book['checked_out_by_last_name'], 'Dahl')

        # Check that checkout timestamp is in mm/dd/yyyy format
        # Get current date in the same format
        expected_date = datetime.now().strftime("%m/%d/%Y")
        self.assertEqual(book['checkout_timestamp'], expected_date)

    # Add checked-out book
    def test_return_book(self):
        book = {'title': 'The Magician\'s Elephant', 'author': 'Kate DiCamillo', 'isbn': '0763680885', 'quantity': 0, 'checked_out_by_first_name': 'Jane', 'checked_out_by_last_name': 'Smith'}
        self.db_manager.books = [book]

        # Return book
        self.inventory_manager.return_book(book)

        # Check quantity is increased by 1
        self.assertEqual(book['quantity'], 1)

        # Check student info is cleared
        self.assertEqual(book['checked_out_by_first_name'], '')
        self.assertEqual(book['checked_out_by_last_name'], '')

    # Add new book with different quantity
    def test_add_book(self):
        new_book = {'title': 'The Magician\'s Elephant', 'author': 'Kate DiCamillo', 'isbn': '0763680885', 'quantity': 4, 'checked_out_by_first_name': '', 'checked_out_by_last_name': ''}
        self.inventory_manager.add_book(new_book)

        # Check new book is in inventory by checking its isbn
        self.assertTrue(any(book['isbn'] == new_book['isbn'] for book in self.db_manager.books))

    # Add book with quantity 0
    def test_check_out_book_out_of_stock(self):
        book = {'title': 'Hatchet', 'author': 'Gary Paulsen', 'isbn': '1416936475', 'quantity': 0, 'checked_out_by_first_name': '', 'checked_out_by_last_name': ''}
        self.db_manager.books = [book]

        # Try to check out the book
        with self.assertRaises(ValueError):
            self.inventory_manager.check_out_book(book, 'The', 'Miraculous Journey')

    # Add book with quantity 1, not checked out
    def test_return_book_not_checked_out(self):
        book = {'title': 'Hatchet', 'author': 'Gary Paulsen', 'isbn': '1416936475', 'quantity': 1, 'checked_out_by_first_name': '', 'checked_out_by_last_name': ''}
        self.db_manager.books = [book]

        # Try to return the book
        with self.assertRaises(ValueError):
            self.inventory_manager.return_book(book)

    # Test writing new book to CSV file, replacing the old content
    def test_csv_write_mode(self):
        new_book = {'title': 'The Test Book', 'author': 'Test Author Name', 'isbn': '1234567890', 'quantity': 1, 'checked_out_by_first_name': '', 'checked_out_by_last_name': ''}

        # Create new file and write book to it
        with open(self.test_inventory_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = new_book.keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(new_book)

        # Check if the new book is in CSV file
        with open(self.test_inventory_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            self.assertTrue(any(row['title'] == 'The Test Book' for row in rows))

if __name__ == '__main__':
    unittest.main()
