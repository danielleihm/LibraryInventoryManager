import csv
from datetime import datetime

"""
Program: LibraryInventoryManager
File: library.py
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
# Initialize library inventory
class LibraryInventoryManager:
    def __init__(self, db_manager, inventory_file="inventory.csv"):
        self.books = []
        self.db_manager = db_manager
        self.inventory_file = inventory_file
        self.load_inventory()

    # Load inventory from CSV file
    def load_inventory(self):
        try:
            with open(self.inventory_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Add columns for student's first name and last name during checkout
                    self.books.append({
                        'title': row['title'],
                        'author': row['author'],
                        'isbn': row['isbn'],
                        'quantity': int(row['quantity']),
                        'checked_out_by_first_name': row.get('checked_out_by_first_name', ''),
                        'checked_out_by_last_name': row.get('checked_out_by_last_name', ''),
                        'checkout_timestamp': row.get('checkout_timestamp', '')
                    })
        # If file does not exist, initialize an empty list
        except FileNotFoundError:
            self.books = []
        # Reset CSV read error
        except csv.Error:
            self.books = []

    # Save inventory back to CSV file
    def save_inventory(self):
        with open(self.inventory_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'author', 'isbn', 'quantity', 'checked_out_by_first_name', 'checked_out_by_last_name', 'checkout_timestamp']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in self.books:
                writer.writerow(book)

    # Search for book by title, return matching book
    def search_books(self, query):
        return [book for book in self.books if query.lower() in book['title'].lower()]

    # Check out book, reduce quantity by 1 and store student info
    def check_out_book(self, book, first_name, last_name):
        if book['quantity'] > 0:
            book['quantity'] -= 1
            book['checked_out_by_first_name'] = first_name
            book['checked_out_by_last_name'] = last_name
            book['checkout_timestamp'] = datetime.now().strftime("%m/%d/%Y")
            # Save updated book info
            self.save_inventory()
        else:
            raise ValueError("This book is currently out of stock.")

    # Return book, increase quantity by 1, clear student info
    def return_book(self, book):
        if book['quantity'] < 1:
            book['quantity'] += 1
            # Clear student first name info
            book['checked_out_by_first_name'] = ''
            # Clear student last name info
            book['checked_out_by_last_name'] = ''
            # Clear date check out
            book['checkout_timestamp'] = ''
            # Save updated book info
            self.save_inventory()
        else:
            raise ValueError("This book has not been checked out.")

    # Add new book to inventory
    def add_book(self, book):
        self.books.append(book)
        # Save updated inventory back to CSV
        self.save_inventory()