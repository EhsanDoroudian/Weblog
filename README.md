# 📝 Django Blog API

A full-featured blog platform built with Django and Django REST Framework. It includes user authentication, blog post and comment functionality, pagination, filtering, and API documentation via Swagger and ReDoc.

---

## 🚀 Features

- 🔐 Custom user model and authentication system
- 📝 Create, update, delete blog posts and comments (via both HTML views and API)
- 📦 REST API with pagination and filtering
- 🧾 Interactive API docs via Swagger and ReDoc
- ☁️ Deployment-ready (tested on PythonAnywhere)
- 📂 Environment-based settings using `.env`
- ⚙️ Static files managed with WhiteNoise

---

## 📁 Project Structure

```
project-root/
├── accounts/            # User authentication app
├── blogs/               # Blog & comment logic
├── config/              # Project settings and URLs
├── templates/           # HTML templates
├── static/              # Static assets
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── manage.py
```

---

## ⚙️ Installation

1. **Clone the repository:**

   ```bash
   git clone <https://github.com/EhsanDoroudian/Weblog.git>
   cd <Weblog>
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate   # Windows: env\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory:

   ```env
   DJANGO_DEBUG=True
   DJANGO_SECRET_KEY=your-secret-key
   ```

5. **Apply migrations & create a superuser:**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

---

## 🌐 Frontend Views

The project also provides HTML views for blog management:

| URL Pattern                | View Description        |
|---------------------------|-------------------------|
| `/blogs/`                 | Blog list               |
| `/blogs/<pk>/`            | Blog detail             |
| `/blogs/create/`          | Create a new blog post  |
| `/blogs/update/<pk>/`     | Update a blog post      |
| `/blogs/delete/<pk>/`     | Delete a blog post      |
| `/blogs/comment/<pk>/`    | Add comment to a post   |

---

## 🔌 API Endpoints

| Endpoint                  | Description                        |
|---------------------------|------------------------------------|
| `/api/blogs/`             | List or create blog posts          |
| `/api/blogs/<pk>/`        | Retrieve, update, delete a post    |
| `/api/comments/`          | List or create comments            |
| `/api/comments/<pk>/`     | Retrieve, update, delete a comment |
| `/swagger/`               | Swagger UI                         |
| `/redoc/`                 | ReDoc UI                           |
| `/swagger.json`           | Raw schema (JSON or YAML)          |

---

## 🌍 Live Website

[https://ehsandrn22.pythonanywhere.com/]

## 📚 API Documentation

Once the server is running, you can access:

- Swagger UI: [`/swagger/`](http://localhost:8000/swagger/)
- ReDoc: [`/redoc/`](http://localhost:8000/redoc/)
- Schema (JSON/YAML): `/swagger.json` or `/swagger.yaml`

---

## 🌐 Deployment (PythonAnywhere)

1. Upload your project to PythonAnywhere.
2. Set up a virtual environment and install requirements.
3. Add environment variables (`.env`) via PA dashboard or manually.
4. Configure WSGI file and static/media paths.
5. Run:

   ```bash
   python manage.py collectstatic
   ```

6. Restart the web app from the dashboard.

---

## 🔒 Security Notes

- Do **not** enable `DEBUG=True` in production.
- Keep your `.env` file secret and out of version control.
- Use HTTPS and set proper `ALLOWED_HOSTS` in production.

---

## 📄 License

This project is licensed under the [BSD License](https://opensource.org/licenses/BSD-3-Clause).