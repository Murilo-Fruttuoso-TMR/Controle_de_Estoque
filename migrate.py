import os
import sys
from pathlib import Path

# Add the project directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.extensions import db
from sqlalchemy import inspect, text

def migrate_database():
    """Add missing columns to existing tables"""
    app = create_app()
    
    with app.app_context():
        # Get database inspector
        inspector = inspect(db.engine)
        
        # Check and add 'brand' column to products table
        products_columns = [col['name'] for col in inspector.get_columns('products')]
        if 'brand' not in products_columns:
            print("Adding 'brand' column to products table...")
            db.session.execute(text('ALTER TABLE products ADD COLUMN brand VARCHAR(100)'))
            db.session.commit()
            print("✓ 'brand' column added successfully!")
        
        # Check and add 'purchases' table if it doesn't exist
        existing_tables = inspector.get_table_names()
        if 'purchases' not in existing_tables:
            print("Creating 'purchases' table...")
            db.create_all()
            print("✓ 'purchases' table created successfully!")
        
        print("\n✓ Database migration completed!")

if __name__ == '__main__':
    migrate_database()
