# Card Collection Manager

A comprehensive desktop application built with Python, Tkinter, and SQLAlchemy to manage your card collections, including inventory and wishlist tracking.

## Features

This card collection management system includes:

1.  **Series Management**:

    - Add, view, and delete series.
    - Cascade deletion for items when their series is deleted.
    - Track company information and shop websites for series.

2.  **Item Status Tracking**:

    - Checkboxes for signature, gilded, and sealed status for both inventory and wishlist items.
    - Robust database schema to preserve detailed item data.

3.  **Detailed Item Viewing**:

    - Dedicated windows to view all details for inventory and wishlist items.
    - Double-click functionality for quick access to item information.
    - Image preview capabilities with support for various formats (PNG, JPG, GIF).

4.  **Editing Functionality**:

    - Edit existing inventory and wishlist items through dedicated forms.
    - Scrollable content areas in edit windows for better usability.

5.  **Filtering and Sorting**:

    - Filter items by ID, name, series, company, and item properties (signature, gilded, sealed).
    - Sort table columns by clicking on headers.
    - Clear filter functionality to reset the view.

6.  **Wishlist System**:

    - Separate tab for managing your wishlist.
    - Track expected prices, shop URLs, notes, and priority for desired items.
    - "Mark as acquired" feature to easily move items from the wishlist to inventory.

7.  **UI Improvements**:
    - Modern tabbed interface (Inventory & Wishlist) for clear organization.
    - Direct links to open series websites or item shop URLs in your browser.
    - Full scrolling interface in main tabs to handle large collections.
    - Custom application icon.

## Installation

There are two ways to use the Card Collection Manager:

**Method 1: Using the Executable (Recommended for Windows Users)**

1.  Download the latest release package (usually a `.zip` file).
2.  Extract the contents of the zip file to a folder on your computer.
3.  Navigate into the extracted folder, then into the `dist` subfolder.
4.  Double-click `Card Collection Manager.exe` to run the application.
    - No Python installation is required.
    - The `storage.db` file (your collection data) and `assets` folder must be kept in the same directory as the executable.

**Method 2: Running from Source**

1.  Ensure you have Python 3.7 or higher installed.
2.  Clone or download this repository.
3.  Open a terminal or command prompt in the project directory.
4.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
5.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6.  Run the application:
    ```bash
    python app.py
    ```

## Usage

- Use the tabs to switch between your **Inventory** and **Wishlist**.
- Use the forms and buttons to **add**, **edit**, or **delete** items and series.
- **Filter** your lists using the provided search, dropdown, and checkbox options.
- **Sort** lists by clicking on column headers.
- **Double-click** an item in the list or use the "View Details" button to see all its information.
- Manage series using the **Add Series** and **Manage Series** buttons in the Inventory tab.
- Use the **Mark as Acquired** button in the Wishlist tab to move items to your inventory.

## Building from Source

If you want to create the executable yourself:

1.  Follow steps 1-5 in "Method 2: Running from Source".
2.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
3.  Generate the application icon (optional, requires Pillow):
    ```bash
    python create_icon.py
    ```
4.  Run PyInstaller using the spec file:
    ```bash
    pyinstaller card_manager.spec
    ```
5.  The executable and necessary files will be located in the `dist` folder.

## Database

The application uses SQLite (`storage.db`) for data storage. This file is created automatically in the application's directory.

## License

This project is open-source and available under the MIT License.
