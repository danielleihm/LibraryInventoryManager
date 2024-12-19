from library import LibraryInventoryManager
from db_manager import DBManager
from gui import LibraryGUI

"""
Program: LibraryInventoryManager
File: main.py
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

def main():
    # Initialize database manager for CSV file
    db_manager = DBManager()

    # Initialize inventory manager with database manager
    inventory_manager = LibraryInventoryManager(db_manager)

    # Start GUI
    gui = LibraryGUI(inventory_manager)
    gui.window.mainloop()

if __name__ == "__main__":
    main()