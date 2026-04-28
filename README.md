# 🎬 Movies Django Project

A Django web application for managing movies, actors, and genres.  
Users can browse and filter movies, while administrators can manage content.

---

## 🚀 Features

- Browse list of movies
- Filter movies by:
  - title
  - genre
  - actor
- User authentication:
  - registration
  - login/logout
- Role-based access:
  - 👤 Users: view and filter movies
  - 🛠️ Admins: add, edit, delete movies
- Image support (movie posters)
- Responsive UI (Bootstrap)

---

## 🧰 Tech Stack

- Python 3
- Django
- SQLite (default database)
- HTML / CSS / Bootstrap

---

## 📥 Installation Guide

### 1. Clone repository
```bash
git clone <URL_REPO>
cd moj_projekt
```

### 2. Create virtual environment
🍏 Mac / Linux
```bash
git clone <URL_REPO>
cd moj_projekt
```

🪟 Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Database setup
```bash
python manage.py migrate
```

### 5. Create admin user
```bash
python manage.py createsuperuser
```

### 6. Run server
```bash
python manage.py runserver
```

### 7. Open in browser
Main app:
```bash
http://127.0.0.1:8000/
```

Admin panel:
```bash
http://127.0.0.1:8000/admin/
```
