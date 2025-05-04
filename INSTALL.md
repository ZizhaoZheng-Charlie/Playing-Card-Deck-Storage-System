# Card Collection Manager - Installation Guide

## Installation Instructions

### Method 1: Using the Executable (Recommended)

1. Navigate to the `dist` folder
2. Run the `Card Collection Manager.exe` file
3. The application should start immediately with no additional setup

### Method 2: Running from Source

If you prefer to run the application from source code:

1. Make sure you have Python 3.7 or higher installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

## Features

This card collection management system includes:

1. **Series Management**:

   - Add, view, and delete series
   - Cascade deletion for items when their series is deleted
   - Company information for series

2. **Item Status Tracking**:

   - Checkboxes for signature, gilded, and sealed status
   - Detailed database schema for preserving item data

3. **Detailed Item Viewing**:

   - Detailed view windows for both inventory and wishlist items
   - Double-click functionality to show all item information
   - Image preview capabilities

4. **Editing Functionality**:

   - Edit both inventory and wishlist items
   - Scrollable content areas in edit windows

5. **Filtering and Sorting**:

   - Filter by ID, name, series, company, and item properties
   - Sort columns by clicking on column headers
   - Clear filter functionality

6. **Wishlist System**:

   - Track expected prices for desired items
   - "Mark as acquired" functionality to move items to inventory

7. **UI Improvements**:
   - Tabbed interface for organization
   - Website links for series and wishlist items
   - Full scrolling interface for large collections

## Troubleshooting

If you encounter any issues:

1. **Database Issues**: The application creates a SQLite database file named `storage.db`. If this file becomes corrupted, rename or delete it and restart the application to create a new one.

2. **Image Loading Problems**: Make sure your image files are in standard formats (PNG, JPG, GIF).

3. **Windows Display Issues**: If the UI appears too small or large, adjust your Windows display scaling settings.

4. **Executable Won't Start**: Make sure you have extracted all files from the zip archive if applicable.

## Uninstallation

To uninstall the application:

1. Delete the application folder
2. The application does not modify the registry or install system-wide components

## Contact Information

For support or feature requests, please contact the developer.
