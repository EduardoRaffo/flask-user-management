# User Management Web App 👤

**Flask web application for managing users with full CRUD functionality, form validation, and a clean UI built with Tailwind CSS**

![Python](https://img.shields.io/badge/Python-3+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-backend-lightgrey?style=flat-square)
![Tailwind](https://img.shields.io/badge/TailwindCSS-UI-38bdf8?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 Problem Statement

Managing user data manually via spreadsheets or raw files is error-prone and tedious. This **Flask app** centralizes user management in a clean web interface — create, edit, search, and delete users with real-time form feedback and validation.

---

## 💡 Why This Project Matters

This project covers the full cycle of a **Python backend web application**: routing, data persistence, form validation, and a responsive UI — all with clean separation of concerns. It demonstrates practical Flask backend development skills that map directly to production web development workflows.

---

## ✨ Features

- ➕ Create new users with form validation
- ✏️ Edit existing user data
- 🗑️ Delete users
- 📋 List all users in a clean table view
- ✅ Form validation with clear error messages
- 🔁 Form persistence — keeps values after validation errors
- 🎨 Tailwind CSS — responsive, modern UI

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3 + Flask |
| **Frontend** | HTML + Jinja2 + Tailwind CSS |
| **Storage** | JSON (file-based) |
| **Validation** | Custom Python validators |

---

## 🚀 Quick Start

```bash
git clone https://github.com/EduardoRaffo/final-test--web--json--flask.git
cd final-test--web--json--flask
pip install -r requirements.txt
python Prueba_Final_Web.py
```

Then open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🏗️ Project Structure

```
├── Prueba_Final_Web.py     # Flask app — routes & views
├── json_users_data.py      # Data access layer (JSON read/write)
├── validations.py          # Form validation logic
├── users_data.json         # Persistent data storage
├── templates/              # Jinja2 HTML templates
├── tailwind.config.js      # Tailwind CSS configuration
└── requirements.txt        # Python dependencies
```

---

## 🎓 Use Cases

- Learning full-cycle Flask backend development (routing, templates, validation, persistence)
- Prototyping user management features before migrating to a full database backend
- Reference project for CRUD patterns in Python/Flask with clean separation of concerns

---

## 🧠 Skills Demonstrated

✅ Backend development with Flask
✅ CRUD operations (Create, Read, Update, Delete)
✅ Form validation and UX error handling
✅ Data persistence (JSON)
✅ Separation of concerns (routes / data / validation)
✅ Frontend styling with Tailwind CSS

---

## 📈 Future Improvements

- [ ] Migrate storage from JSON to SQLite / SQLAlchemy
- [ ] Add user authentication and sessions
- [ ] REST API endpoints
- [ ] Deploy to cloud (Render / Railway)
- [ ] Pagination and search

---

## 📄 License

MIT License — free for educational and personal use.

---

## 👤 Author

**Eduardo Raffo** — Python Backend Developer (Junior)
- GitHub: [github.com/EduardoRaffo](https://github.com/EduardoRaffo)
- LinkedIn: [linkedin.com/in/eduardo-raffo-benitez](https://linkedin.com/in/eduardo-raffo-benitez)
