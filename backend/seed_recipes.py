#!/usr/bin/env python3
"""
Seed Recipes Script
This script loads recipes from the sample_recipes.json file and adds them to the MongoDB database.
"""

import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from datetime import datetime
import json


def seed_recipes(mongo_uri='mongodb://localhost:27017/', db_name='food_recipe_db'):
    """
    Seed the database with recipes from sample_recipes.json.
    
    Args:
        mongo_uri: MongoDB connection string
        db_name: Name of the database
    
    Returns:
        int: Number of recipes added
    """
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        recipes_collection = db['recipes']
        
        # Load recipes from JSON file
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'sample_recipes.json')
        
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            sample_recipes = data.get('recipes', [])
        
        # Add timestamps to each recipe
        for recipe in sample_recipes:
            recipe['created_at'] = datetime.utcnow()
            recipe['updated_at'] = datetime.utcnow()
        
        # Clear existing recipes and insert new ones
        recipes_collection.delete_many({})
        result = recipes_collection.insert_many(sample_recipes)
        
        print(f"Successfully added {len(result.inserted_ids)} recipes to the database!")
        print(f"Database: {db_name}")
        print(f"Collection: recipes")
        
        # Display the recipes
        print("\nRecipes added:")
        for i, recipe in enumerate(sample_recipes, 1):
            print(f"  {i}. {recipe['name']} ({recipe['cuisine']}) - {recipe['difficulty']} - {recipe['cooking_time']} min")
        
        client.close()
        return len(result.inserted_ids)
        
    except FileNotFoundError:
        print(f"Error: Could not find sample_recipes.json at {json_file_path}")
        return 0
    except Exception as e:
        print(f"Error seeding recipes: {e}")
        return 0


if __name__ == '__main__':
    # Allow command line arguments for custom MongoDB URI and database name
    mongo_uri = sys.argv[1] if len(sys.argv) > 1 else 'mongodb://localhost:27017/'
    db_name = sys.argv[2] if len(sys.argv) > 2 else 'food_recipe_db'
    
    print("=" * 60)
    print("Food Recipe System - Database Seeding")
    print("=" * 60)
    
    count = seed_recipes(mongo_uri, db_name)
    
    if count > 0:
        print("\nDatabase seeded successfully!")
        sys.exit(0)
    else:
        print("\nFailed to seed database!")
        sys.exit(1)
