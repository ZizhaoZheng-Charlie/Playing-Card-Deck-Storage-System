import sqlite3
from sqlalchemy import create_engine, inspect
from models import Base, Session, Item, Series, WishItem


def migrate_database():
    print("Starting database migration...")

    # Connect to the database
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()

    # Backup existing data
    print("Backing up existing data...")

    # Get series data
    cursor.execute("SELECT id, name, shop_website, company_name FROM series")
    series_data = cursor.fetchall()

    # Get items data (only retrieving columns that existed in original schema)
    try:
        cursor.execute(
            "SELECT id, name, series_id, quantity, image, image_name FROM items"
        )
        items_data = cursor.fetchall()
    except sqlite3.OperationalError:
        print(
            "Items table might have a different structure, trying alternative query..."
        )
        try:
            cursor.execute("PRAGMA table_info(items)")
            columns = [info[1] for info in cursor.fetchall()]

            query = f"SELECT id, name, series_id, quantity, {', '.join(['image' if 'image' in columns else 'NULL', 'image_name' if 'image_name' in columns else 'NULL'])} FROM items"
            cursor.execute(query)
            items_data = cursor.fetchall()
        except:
            print("Could not retrieve items data, will create empty items table")
            items_data = []

    # Close the connection
    conn.close()

    # Drop all tables and recreate schema
    print("Recreating database schema...")
    engine = create_engine("sqlite:///storage.db")

    # Drop tables if they exist
    Base.metadata.drop_all(engine)

    # Create tables with new schema
    Base.metadata.create_all(engine)

    # Create a session
    session = Session()

    # Restore series data
    print(f"Restoring {len(series_data)} series records...")
    for series_record in series_data:
        series = Series(
            id=series_record[0],
            name=series_record[1],
            shop_website=series_record[2] if series_record[2] else None,
            company_name=series_record[3] if series_record[3] else None,
        )
        session.add(series)

    # Commit series to get IDs
    session.commit()

    # Restore items data with new default values for missing columns
    print(f"Restoring {len(items_data)} item records...")
    for item_record in items_data:
        # Handle potential NULL values in the data
        image_data = item_record[4] if len(item_record) > 4 and item_record[4] else None
        image_name = item_record[5] if len(item_record) > 5 and item_record[5] else None

        item = Item(
            id=item_record[0],
            name=item_record[1],
            series_id=item_record[2],
            quantity=item_record[3] if item_record[3] else 0,
            image=image_data,
            image_name=image_name,
            # Set default values for new columns
            is_signature=False,
            is_gilded=False,
            is_sealed=False,
        )
        session.add(item)

    # Commit all changes
    session.commit()
    session.close()

    print("Migration completed successfully!")


if __name__ == "__main__":
    migrate_database()
