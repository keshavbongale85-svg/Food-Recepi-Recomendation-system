# MongoDB Schema Documentation

## Database: `food_recipe_db`

This document describes the MongoDB collections and their schemas for the Food Recipe Recommendation System.

---

## Collection: `users`

Stores user account information.

### Document Structure

```json
{
    "_id": ObjectId("..."),
    "username": "string",
    "email": "string",
    "password": "string (hashed)",
    "created_at": ISODate("..."),
    "updated_at": ISODate("...")
}
```

### Example Document

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "username": "johndoe",
    "email": "john@example.com",
    "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    "created_at": ISODate("2024-01-15T10:30:00Z"),
    "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Indexes

- `email` (unique)
- `username` (unique)

---

## Collection: `recipes`

Stores all recipe information.

### Document Structure

```json
{
    "_id": ObjectId("..."),
    "name": "string",
    "ingredients": ["string"],
    "steps": ["string"],
    "category": "string (veg/non-veg/vegan)",
    "cuisine": "string",
    "image_url": "string",
    "cooking_time": number (minutes),
    "difficulty": "string (Easy/Medium/Hard)",
    "created_at": ISODate("..."),
    "updated_at": ISODate("...")
}
```

### Example Document

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439012"),
    "name": "Vegetable Biryani",
    "ingredients": ["rice", "vegetables", "onion", "garlic", "ginger", "spices", "saffron", "ghee"],
    "steps": [
        "Soak rice for 30 minutes",
        "Fry onions until golden",
        "Add vegetables and spices",
        "Layer rice and vegetables",
        "Cook on low heat for 20 minutes"
    ],
    "category": "veg",
    "cuisine": "Indian",
    "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400",
    "cooking_time": 45,
    "difficulty": "Medium",
    "created_at": ISODate("2024-01-15T10:30:00Z"),
    "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Indexes

- `category`
- `cuisine`
- `ingredients` (text search)

---

## Collection: `user_preferences`

Stores user food preferences for personalized recommendations.

### Document Structure

```json
{
    "_id": ObjectId("..."),
    "user_id": ObjectId("..."),
    "dietary_preferences": ["string (veg/non-veg/vegan)"],
    "favorite_cuisines": ["string"],
    "disliked_ingredients": ["string"],
    "created_at": ISODate("..."),
    "updated_at": ISODate("...")
}
```

### Example Document

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439013"),
    "user_id": ObjectId("507f1f77bcf86cd799439011"),
    "dietary_preferences": ["veg"],
    "favorite_cuisines": ["Indian", "Italian"],
    "disliked_ingredients": ["paneer", "mushroom"],
    "created_at": ISODate("2024-01-15T10:30:00Z"),
    "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Indexes

- `user_id` (unique)

---

## Sample Queries

### Create User

```javascript
db.users.insertOne({
    username: "johndoe",
    email: "john@example.com",
    password: "hashed_password_here",
    created_at: new Date(),
    updated_at: new Date()
})
```

### Create Recipe

```javascript
db.recipes.insertOne({
    name: "Vegetable Biryani",
    ingredients: ["rice", "vegetables", "onion", "garlic", "ginger", "spices", "saffron", "ghee"],
    steps: ["Soak rice for 30 minutes", "Fry onions until golden", "Add vegetables and spices"],
    category: "veg",
    cuisine: "Indian",
    image_url: "https://example.com/image.jpg",
    cooking_time: 45,
    difficulty: "Medium",
    created_at: new Date(),
    updated_at: new Date()
})
```

### Search Recipes by Ingredients

```javascript
db.recipes.find({
    ingredients: { $regex: "chicken|garlic", $options: "i" }
})
```

### Get User Preferences

```javascript
db.user_preferences.findOne({
    user_id: ObjectId("507f1f77bcf86cd799439011")
})
```
