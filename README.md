# Banking-System-AP-Project

This repository contains the implementation of a basic banking system developed as a university project. The project allows users to perform various banking operations such as account management, money transfers, and loan processing. The system uses a text-based interface and stores data in text files.

## Features

- **User Registration**: Register users with personal information (name, national ID, password, phone number, email).
- **User Login**: Log in with national ID and password.
- **Account Management**:
  - Create and manage multiple bank accounts.
  - View account balance and transaction history.
  - Manage multiple accounts and assign aliases for frequent accounts.
- **Money Transfer**: Transfer money between accounts.
- **Bill Payment**: Pay bills by entering bill and payment identifiers.
- **Loan Request**: Request loans, with automatic deduction of installments.
- **Admin Portal**: An admin can:
  - View all customer accounts.
  - Modify user information.
  - Open and close user accounts.
  
## Files

- **`main.py`**: The main script to run the banking application.
- **`Database.py`**: Handles database interactions and operations (insert, update, delete, select).
- **`Total.py`**: Additional utilityfor the system.
- **`schema.txt`**: Defines the structure of the database (tables, columns, and data types).
- **`accounts.txt`**: Stores account details (account numbers, balances, etc.).
- **`users.txt`**: Stores user details (ID, password, personal information).
- **`transactions.txt`**: Logs all transactions (deposits, withdrawals, transfers).
- **`debts.txt`**: Stores information about users' loan and debt details.
- **`tickets.txt`**: Stores information about customer support tickets or queries.
- **`id_numbers.txt`**: Stores generated unique ID numbers for users.
- **`tables_info.txt`**: Contains metadata about the database tables.

