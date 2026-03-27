"""
Database Configuration Module
This module handles the MongoDB connection for the Food Recipe Recommendation System.
"""

from pymongo import MongoClient
from flask import Flask

def init_db(app: Flask):
    """
    Initialize MongoDB database connection.
    
    Args:
        app: Flask application instance
        
    Returns:
        MongoClient: MongoDB client instance
    """
    # MongoDB connection string - update with your local MongoDB details
    # Default: localhost on port 27017
    mongo_uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/')
    db_name = app.config.get('MONGO_DB', 'food_recipe_db')
    
    # Create MongoDB client
    client = MongoClient(mongo_uri)
    
    # Connect to the database
    db = client[db_name]
    
    return client, db


def get_database():
    """
    Get the database instance.
    
    Returns:
        Database: MongoDB database instance
    """
    from app import app
    client, db = init_db(app)
    return db
