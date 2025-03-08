# Storage Management System

A Python-based storage management system with GUI interface that allows you to manage items with their names, series, quantities, and associated images.

## Features

- Add items with names, series, and quantities
- Upload and store images for each item
- View all items in a sortable table
- Delete items from the database
- SQLite database backend for persistent storage
- Modern GUI interface using tkinter

## Requirements

- Python 3.7 or higher
- Required packages (install using pip):
  ```
  pip install -r requirements.txt
  ```

## Setup

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```

## Usage

1. **Adding Items**:

   - Fill in the item details (name, series, quantity)
   - Click "Select Image" to add an image (optional)
   - Click "Add Item" to save to the database

2. **Viewing Items**:

   - All items are displayed in the table below the input form
   - Click on column headers to sort items

3. **Deleting Items**:

   - Select an item from the table
   - Click "Delete Selected" to remove it
   - Confirm the deletion when prompted

4. **Refreshing the List**:
   - Click "Refresh List" to update the table with the latest data

## Database

The application uses SQLite for data storage. The database file (`storage.db`) is created automatically when you first run the application.

## License

This project is open-source and available under the MIT License.
