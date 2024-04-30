## PostgreSQL Data Management and Table Generation with Python

This project involves managing data and interacting with a PostgreSQL database using Python. The goal is to generate a bilan table based on data from an Excel file. The project consists of two main files: `source.py` and `app.py`.

### source.py

This file contains functions for connecting to a PostgreSQL database, reading data from an Excel file, and filling tables in the database. Here's a brief overview of the functions:

- `connect_db(dbname, user, password, host, port)`: Connects to a PostgreSQL database with the given parameters and returns a connection object and a cursor object.
- `disconnect_db()`: Closes the connection to the PostgreSQL database.
- `create_tables()`: Creates the necessary tables in the database.
- `drop_tables()`: Drops the tables from the database.
- `read_data(excel_path)`: Reads data from an Excel file and stores it in a global variable.
- `fill_achat_table()`, `fill_artice_table()`, `fill_vent_table()`, `fill_bilan_table()`: Fills the respective tables in the database with data from the global variable.

### app.py

This file contains a GUI application built using the Tkinter library. The application allows the user to connect to a PostgreSQL database, read data from an Excel file, and generate the bilan table. Here's a brief overview of the functions:

- `Application()`: Initializes the Tkinter application and sets up the GUI.
- `connect()`: Connects to a PostgreSQL database using the input from the user.
- `disconnect()`: Closes the connection to the PostgreSQL database.
- `read_data()`: Allows the user to select an Excel file and reads the data.
- `create_tables()`: Creates the necessary tables in the database.
- `fill_tables()`: Fills the tables in the database with data from the Excel file.
- `generate_bilan()`: Generates the bilan table in the database.

### How to run the project

To run the project, simply execute the `app.py` file. The user will be presented with a GUI that allows them to connect to a PostgreSQL database, read data from an Excel file, and generate the bilan table.

