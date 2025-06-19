from app import db
from app.models.offer_letter import OfferLetter

def create_offer_letters_table():
    """
    Create the offer_letters table in the database.
    Run this script after adding the OfferLetter model.
    """
    print("Creating offer_letters table...")
    db.create_all()
    print("Table created successfully!")

if __name__ == "__main__":
    create_offer_letters_table()
