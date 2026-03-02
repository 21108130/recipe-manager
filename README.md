# 🍳 Recipe Manager - Django Full Stack Application

![Django](https://img.shields.io/badge/Django-6.0.2-green)
![Python]
## ✨ Features

### 🔐 User Authentication
- User registration and login system
- Profile management with profile pictures
- Secure password handling

### 📝 Recipe Management
- Create, read, update, and delete recipes
- Upload recipe images
- Categorize recipes (Breakfast, Lunch, Dinner, etc.)
- Like/unlike favorite recipes

### 🌐 Web Scraping Integration
- Automatically fetch recipes from popular websites:
  - Food Network
  - BBC Good Food
  - Tasty
  - Allrecipes
- Extract complete recipe details (ingredients, instructions, images)
- Fallback mechanism when scraping fails

### 🔍 Search & Filter
- Search recipes in local database
- Search recipes from the web
- Filter recipes by category
- View both local and web recipes in one place

### 📱 Responsive Design
- Mobile-friendly interface
- Bootstrap 5 with custom CSS
- Smooth animations and hover effects
- Food-themed color scheme

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django 6.0** | Backend framework |
| **Python 3.12** | Programming language |
| **SQLite** | Database |
| **Bootstrap 5** | Frontend styling |
| **BeautifulSoup4** | Web scraping |
| **Requests** | HTTP requests |
| **Pillow** | Image processing |

## 📂 Project Structure
recipe_manager/
├── manage.py # Django command center
├── requirements.txt # Project dependencies
├── db.sqlite3 # Database
├── media/ # Uploaded images
│ ├── profile_pics/ # User profile pictures
│ └── recipe_pics/ # Recipe images
├── static/ # CSS/JS files
├── templates/ # HTML templates
│ ├── base.html # Base template
│ ├── registration/ # Auth templates
│ └── recipes/ # Recipe templates
├── recipe_manager/ # Project settings
│ └── settings.py # Configuration
└── recipes/ # Main app
├── models.py # Database models
├── views.py # Business logic
├── urls.py # URL routing
├── forms.py # Form handling
├── admin.py # Admin panel
└── utils/ # Utilities
└── scraper.py # Web scraping

text

## 🚀 Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/21108130/recipe-manager.git
   cd recipe-manager
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies

bash
pip install -r requirements.txt
Apply migrations

bash
python manage.py makemigrations
python manage.py migrate
Create superuser

bash
python manage.py createsuperuser
Create media folders

bash
mkdir media\profile_pics media\recipe_pics
Run development server

bash
python manage.py runserver
Access the application

Main site: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin

🎯 Usage Guide
For Regular Users
Sign up for a new account

Login with your credentials

Browse categories on the homepage

Search for recipes using the search bar

View recipe details by clicking on any recipe

Like your favorite recipes

Create your own recipes using the "Add Recipe" button

Edit/Delete your recipes from your profile

For Admin Users
Access the admin panel at /admin

Manage users, recipes, and categories

Monitor site activity

🤝 How It Works
Local Recipe Storage
text
User → Creates Recipe → Saves to Database → Available to All Users
Web Scraping Flow
text
User Searches → Scraper Fetches from Websites → Extracts Recipe Data → Displays Results
Authentication Flow
text
User Signs Up → Profile Created → Can Create/Like Recipes → Data Persists
📊 Database Schema
🔮 Future Enhancements
User following system

Recipe ratings (1-5 stars)

Comments on recipes

Shopping list generator

Meal planner

Nutritional information

Recipe recommendations based on likes

Social sharing

🐛 Known Issues & Solutions
Issue	Solution
Food Network 403 error	Added multiple user agents and fallback sources
Duplicate web recipes	Implemented deduplication logic
Slow web search	Added caching with Redis
Image upload fails	Increased media file size limit
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a new branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

👩‍💻 Author
Maira Javed

GitHub: @21108130

LinkedIn: [Maira Javed](https://www.linkedin.com/in/maira-javed-34bba7373/)

Email: mahijaved@gmail.com
