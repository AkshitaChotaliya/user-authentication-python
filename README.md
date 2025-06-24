
🔐 Django Authentication API
A basic and extendable user authentication system built with Django and Django REST Framework. This project demonstrates:

* User registration (signup)

* Admin panel customization

* Password handling

* Database rollback on failure

* RESTful API endpoints using Django REST Framework (DRF)

🔧 Tech Stack
Backend: Django, Django REST Framework

Database: SQLite (default)

Language: Python 3.10+

* Send a welcome email asynchronously after a user signs up.
.

✉️ Send Welcome Email Asynchronously with Celery
📦 Setup Requirements
* Django

* Celery

* Redis (as broker)

* django-celery-results (for storing task results in DB – optional but recommended)

Run the celery command:

* redis-server
* celery -A myproject worker --loglevel=info
* django_celery_results table using migrate command to migrate


## 📁 Project Structure

```
myproject/
├── myapp/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── config.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── myproject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## 🚀 Running the Project

### 1. Clone the repository (if applicable)

```bash
git clone <your-repo-url>
cd myproject
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

### 6. Test the Signup API

Endpoint: `POST /api/auth/signup/`

Request Body:
```json
{
  "username": "akshita",
  "email": "akshita@example.com",
  "password": "Secure123"
}
```

---

## ✅ Features

- Signup with token support
- Uses Django built-in `User` model
- Easy to extend with JWT login, password reset, etc.

---

## 📌 Note

Make sure to include `rest_framework` in your `INSTALLED_APPS` inside `settings.py`.

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'myapp',
]
```

---

## 🧩 To Do

- Add JWT login and token refresh
- Add password reset functionality
- Protect views with authentication

---

## License

MIT
