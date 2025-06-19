import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.offer_letter import OfferLetter

def create_offer_letters_table():
    """
    Create the offer_letters table in the database.
    Run this script after adding the OfferLetter model.
    """
    print("Creating offer_letters table...")
    app = create_app()
    with app.app_context():
        db.create_all()
    print("Table created successfully!")

if __name__ == "__main__":
    create_offer_letters_table()
