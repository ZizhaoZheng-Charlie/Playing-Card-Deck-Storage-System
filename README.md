# Storage Management System

A Python-based storage management system with a graphical user interface (GUI) built using Tkinter and SQLAlchemy. It allows you to manage an inventory of items, track a wishlist, and store details including images and associated series information.

## Features

- **Tabbed Interface:** Manage inventory and wishlist in separate tabs.
- **Inventory Management:**
    - Add items with name, series, quantity, image, and status (signature, gilded, sealed).
    - Edit existing items.
    - Delete items.
    - View items in a sortable table.
    - Image preview for selected items.
- **Series Management:**
    - Add new series with name, company, and website URL.
    - Manage existing series (view, delete).
    - Link items to series.
    - Open series website directly from inventory or series management.
- **Wishlist Management:**
    - Add items you want to acquire with name, series, expected price, shop URL, notes, priority, and status (signature, gilded, sealed).
    - Edit wishlist items.
    - Delete wishlist items.
    - Mark items as acquired, moving them to the inventory.
    - View wishlist items in a sortable table.
    - View notes for selected wishlist items.
    - Open shop URL directly from the wishlist.
- **Item Details View:**
    - Double-click any item (inventory or wishlist) to view all its details in a dedicated window.
- **Database:**
    - Uses SQLite for persistent storage (`storage.db`).
    - SQLAlchemy ORM for database interactions.

## Requirements

- Python 3.7 or higher
- Required packages (install using pip):
  ```bash
  pip install -r requirements.txt
  ```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Initialize/Migrate Database:**
    - The first time you run `app.py`, the database (`storage.db`) and tables will be created automatically.
    - If you encounter schema errors after updates (e.g., `no such column`), run the migration script:
      ```bash
      python migrate_db.py
      ```
5.  **Run the application:**
    ```bash
    python app.py
    ```

## Usage

- Use the **Inventory** tab to manage items you own.
- Use the **Wishlist** tab to track items you want to buy.
- **Adding Items/Wish Items:** Use the forms and buttons provided in each tab.
- **Managing Series:** Use the "Add Series" and "Manage Series" buttons in the Inventory tab's input section.
- **Viewing Details:** Double-click an item in either list or select it and click "View Details".
- **Editing:** Select an item and click "Edit Selected".
- **Deleting:** Select an item and click "Delete Selected".
- **Websites/URLs:** Use the dedicated buttons or double-click items (in some views) to open associated websites.

## Database Schema Updates

If the database schema changes (e.g., new columns are added to tables in `models.py`), you might need to update your existing `storage.db` file. Run the migration script provided:

```bash
python migrate_db.py
```

This script attempts to back up existing data, recreate the tables with the new schema, and restore the data.

## License

This project is open-source and available under the MIT License.
