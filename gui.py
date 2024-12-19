import tkinter as tk
from tkinter import messagebox

"""
Program: LibraryInventoryManager
File: gui.py
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
class LibraryGUI:
    # Initialize GUI
    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager
        self.window = tk.Tk()
        self.window.title("Library Inventory Manager")
        self.create_widgets()

    def create_widgets(self):
        # Search Books Section
        search_frame = tk.Frame(self.window)
        search_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='w')

        self.search_label = tk.Label(search_frame, text="Search Books by Title:")
        self.search_label.grid(row=0, column=0, padx=10)

        self.search_entry = tk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=10)

        self.search_button = tk.Button(search_frame, text="Search", command=self.search_books)
        self.search_button.grid(row=0, column=2, padx=10)

        # Book List Box
        self.book_listbox = tk.Listbox(self.window, width=50, height=10)
        self.book_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Student Info Section
        student_info_frame = tk.Frame(self.window)
        student_info_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.student_info_label = tk.Label(student_info_frame, text="Student Information:")
        self.student_info_label.grid(row=0, column=0, columnspan=2)

        self.first_name_label = tk.Label(student_info_frame, text="First Name:")
        self.first_name_label.grid(row=1, column=0, padx=10)

        self.first_name_entry = tk.Entry(student_info_frame)
        self.first_name_entry.grid(row=1, column=1, padx=10)

        self.last_name_label = tk.Label(student_info_frame, text="Last Name:")
        self.last_name_label.grid(row=2, column=0, padx=10)

        self.last_name_entry = tk.Entry(student_info_frame)
        self.last_name_entry.grid(row=2, column=1, padx=10)

        # Checkout/Return Section
        action_frame = tk.Frame(self.window)
        action_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.checkout_button = tk.Button(action_frame, text="Check Out", command=self.check_out_book, width=15)
        self.checkout_button.grid(row=0, column=0, padx=10)

        self.return_button = tk.Button(action_frame, text="Return Book", command=self.return_book, width=15)
        self.return_button.grid(row=0, column=1, padx=10)

        # Add New Book Section
        add_book_frame = tk.Frame(self.window)
        add_book_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.add_book_label = tk.Label(add_book_frame, text="Add New Book:")
        self.add_book_label.grid(row=0, column=0, columnspan=2)

        self.new_author_label = tk.Label(add_book_frame, text="Author:")
        self.new_author_label.grid(row=2, column=0, padx=10)

        self.new_author_entry = tk.Entry(add_book_frame)
        self.new_author_entry.grid(row=2, column=1, padx=10)

        self.new_isbn_label = tk.Label(add_book_frame, text="ISBN:")
        self.new_isbn_label.grid(row=3, column=0, padx=10)

        self.new_isbn_entry = tk.Entry(add_book_frame)
        self.new_isbn_entry.grid(row=3, column=1, padx=10)

        self.new_title_label = tk.Label(add_book_frame, text="Title:")
        self.new_title_label.grid(row=1, column=0, padx=10)

        self.new_title_entry = tk.Entry(add_book_frame)
        self.new_title_entry.grid(row=1, column=1, padx=10)

        self.new_quantity_label = tk.Label(add_book_frame, text="Quantity:")
        self.new_quantity_label.grid(row=4, column=0, padx=10)

        self.new_quantity_entry = tk.Entry(add_book_frame)
        self.new_quantity_entry.grid(row=4, column=1, padx=10)

        self.add_button = tk.Button(add_book_frame, text="Add Book", command=self.add_new_book, width=15)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Search books
    def search_books(self):
        query = self.search_entry.get()
        # Store search results
        self.search_results = self.inventory_manager.search_books(query)
        self.book_listbox.delete(0, tk.END)
        for book in self.search_results:
            self.book_listbox.insert(tk.END, f"{book['title']} by {book['author']}")

    # Check out book
    def check_out_book(self):
        selected_book = self.book_listbox.curselection()
        if selected_book:
            # Use search results for selected book
            book = self.search_results[selected_book[0]]
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()

            # Validate student name fields
            if not first_name or not last_name:
                messagebox.showwarning("Input Error", "Please enter both first and last name.")
                return

            # Check if book is available to check out
            if book['quantity'] > 0:
                # Process book check out
                self.inventory_manager.check_out_book(book, first_name, last_name)
                # Refresh list
                self.search_books()
                messagebox.showinfo("Success", "Book checked out successfully!")
            else:
                messagebox.showwarning("Warning", "This book is out of stock.")
        else:
            messagebox.showwarning("Warning", "Please select a book to check out.")

    # Return book
    def return_book(self):
        selected_book = self.book_listbox.curselection()
        if selected_book:
            # Use search_results for selected book
            book = self.search_results[selected_book[0]]

            # Check if book is currently checked out, if quantity < 1 then checked out
            if book['quantity'] < 1:
                # Process book return
                self.inventory_manager.return_book(book)
                # Refresh list
                self.search_books()
                messagebox.showinfo("Success", "Book returned successfully!")
            else:
                messagebox.showwarning("Warning", "This book has not been checked out.")
        else:
            messagebox.showwarning("Warning", "Please select a book to return.")

    # Add new book
    def add_new_book(self):
        # Getters to retrieve book information
        title = self.new_title_entry.get()
        author = self.new_author_entry.get()
        isbn = self.new_isbn_entry.get()
        quantity = self.new_quantity_entry.get()

        # Check input fields are completed
        if not isbn or not title or not author or not quantity:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # Convert quantity input to int
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be a number.")
            return

        # Create dictionary with new book info
        new_book = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'quantity': quantity
        }

        # Add new book to inventory with inventory manager
        self.inventory_manager.add_book(new_book)

        # Refresh book list
        self.search_books()

        # Clear input fields after adding book
        self.new_title_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_isbn_entry.delete(0, tk.END)
        self.new_quantity_entry.delete(0, tk.END)

        # Message that book was successfully added
        messagebox.showinfo("Success", "New book added to the inventory.")