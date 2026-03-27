# Food Recipe Recommendation System

A full-stack web application that recommends recipes based on ingredients, food category, and cuisine type. Built using Python (Flask), MongoDB, HTML, CSS, and JavaScript.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Recommendation Logic](#recommendation-logic)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

This is a **Food Recipe Recommendation System** designed for college mini projects. Users can:
- Register and login
- Search for recipes based on ingredients they have
- Filter by category (Veg/Non-Veg/Vegan)
- Filter by cuisine type
- View detailed recipe instructions
- Get similar recipe recommendations

---

## ✨ Features

### User Management
- User registration with email and password
- Secure login/logout functionality
- Session management

### Recipe Search
- Search by multiple ingredients
- Filter by food category (Veg, Non-Veg, Vegan)
- Filter by cuisine type (Indian, Italian, Chinese, etc.)
- Smart scoring based on ingredient matches

### Recipe Details
- View complete recipe with ingredients
- Step-by-step cooking instructions
- Cooking time and difficulty level
- Recipe images

### Recommendations
- Similar recipe suggestions
- Personalized recommendations based on preferences
- Match percentage scoring

---

## 📂 Project Structure

```
food-recipe-system/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── database.py         # MongoDB connection
│   ├── models.py           # Database models
│   ├── routes.py           # API routes
│   ├── recommendation.py   # Recommendation engine
│   ├── requirements.txt    # Python dependencies
│   └── templates/          # HTML templates
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── search.html
│       ├── recipes.html
│       └── recipe_detail.html
├── frontend/
│   ├── css/
│   │   └── style.css       # Responsive styles
│   └── js/
│       ├── main.js         # Common utilities
│       ├── auth.js         # Authentication
│       ├── search.js       # Recipe search
│       └── recipes.js      # Recipe listing
├── data/
│   ├── sample_recipes.json # Sample data
│   └── mongodb_schema.md   # Database schema
└── README.md               # This file
```

---

## 🛠 Technology Stack

### Backend
- **Python 3.x** - Programming language
- **Flask** - Web framework
- **PyMongo** - MongoDB driver
- **Flask-CORS** - Cross-origin support

### Database
- **MongoDB** - NoSQL database

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling
- **JavaScript (ES6+)** - Client-side logic
- **Fetch API** - API communication

---

## 📌 Prerequisites

Before running this project, ensure you have:

1. **Python 3.7+** installed
2. **MongoDB** installed and running locally (or use MongoDB Atlas)
3. **Web browser** (Chrome, Firefox, Edge)

---

## 🚀 Installation Steps

### Step 1: Install Python Dependencies

Navigate to the backend directory and install required packages:

```bash
cd food-recipe-system/backend
pip install -r requirements.txt
```

### Step 2: Start MongoDB

Make sure MongoDB is running. If using local MongoDB:

```bash
# On Windows (in cmd)
net start MongoDB

# On Linux/Mac
sudo systemctl start mongod
```

Or use MongoDB Atlas (cloud) and update the connection string in `app.py`.

### Step 3: Run the Flask Application

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`

### Step 4: Seed Sample Recipes

Open your browser and visit:
```
http://127.0.0.1:5000/api/seed_recipes
```

This will add 12 sample recipes to the database.

---

## ▶️ How to Run

1. **Start MongoDB** (ensure it's running on localhost:27017)

2. **Start the Flask server**:
   ```bash
   cd food-recipe-system/backend
   python app.py
   ```

3. **Open your browser** and navigate to:
   - Home: http://127.0.0.1:5000/
   - Login: http://127.0.0.1:5000/login
   - Register: http://127.0.0.1:5000/register
   - Search: http://127.0.0.1:5000/search
   - All Recipes: http://127.0.0.1:5000/recipes

4. **Test the application**:
   - Register a new account
   - Login with your credentials
   - Search for recipes using ingredients
   - Browse all recipes
   - View recipe details

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register a new user |
| POST | `/api/login` | Login user |
| POST | `/api/logout` | Logout user |
| GET | `/api/check_session` | Check login status |

### Recipes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/recipes` | Get all recipes |
| GET | `/api/recipes/<id>` | Get recipe by ID |
| POST | `/api/recipes/search` | Search recipes |
| GET | `/api/recipes/category/<cat>` | Get by category |
| GET | `/api/recipes/cuisine/<cuisine>` | Get by cuisine |
| GET | `/api/recipes/<id>/similar` | Get similar recipes |
| POST | `/api/seed_recipes` | Add sample recipes |

### Preferences
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/preferences` | Get user preferences |
| PUT | `/api/preferences` | Update preferences |

---

## 🧮 Recommendation Logic

The recommendation system uses a **scoring algorithm** to rank recipes:

### Scoring Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| Ingredient Match | +30 per ingredient | For each matching ingredient |
| Category Match | +25 | If category matches user preference |
| Cuisine Match | +20 | If cuisine matches user preference |
| Favorite Cuisine Bonus | +15 | If cuisine is in user's favorites |
| Disliked Ingredients | -50 | Penalty for disliked ingredients |
| Category Mismatch | -30 | Penalty for wrong category |

### Formula

```
Score = (Matched Ingredients × 30) + (Category Match × 25) + (Cuisine Match × 20) 
      + (Favorite Cuisine Bonus × 15) - (Disliked Penalty) - (Category Mismatch Penalty)
```

### Example

User searches with:
- Ingredients: ["chicken", "garlic", "tomatoes"]
- Category: "non-veg"
- Cuisine: "Indian"

Recipe: Butter Chicken
- Matches: chicken (+30), garlic (+30), tomatoes (+30)
- Category: non-veg (+25)
- Cuisine: Indian (+20)
- **Total Score: 135**

---

## 📸 Screenshots

The application features:
- Modern, responsive design
- Clean navigation bar
- Ingredient tag input system
- Recipe cards with images
- Detailed recipe view with step-by-step instructions

---

## 🔮 Future Enhancements

- User ratings and reviews
- Save favorite recipes
- Shopping list generation
- Meal planning features
- Social sharing
- Admin panel for recipe management
- Image upload for recipes
- Email notifications
- Mobile app support

---

## 📝 License

This project is created for educational purposes as a college mini project.

---

## 👨‍💻 Author

Created as a demonstration project for learning full-stack development with Python, Flask, and MongoDB.

---

## 📞 Support

For issues or questions:
1. Check MongoDB is running
2. Verify Python dependencies are installed
3. Check the console for error messages

---

**Happy Cooking! 🍳**
