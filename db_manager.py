import csv

"""
Program: LibraryInventoryManager
File: db_manager.py
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
# Initialize inventory file
class DBManager:
    def __init__(self, inventory_file="inventory.csv"):
        self.inventory_file = inventory_file

    # Load library inventory (reader)
    def load_inventory(self):
        books = []
        try:
            with open(self.inventory_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    books.append({
                        'title': row['title'],
                        'author': row['author'],
                        'isbn': row['isbn'],
                        'quantity': int(row['quantity']),
                        'checked_out_to_first_name': row.get('checked_out_to_first_name', ''),
                        'checked_out_to_last_name': row.get('checked_out_to_last_name', ''),
                        'checkout_timestamp': row.get('checkout_timestamp', '')
                    })
        except FileNotFoundError:
            books = []
        except csv.Error:
            books = []
        return books

    # Save library inventory (writer)
    def save_inventory(self, books):
        with open(self.inventory_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'author', 'isbn', 'quantity', 'checked_out_to_first_name', 'checked_out_to_last_name', 'checkout_timestamp']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in books:
                writer.writerow(book)