```markdown
# FastAPI Multi-Tenant Project Management API

This project is a **multi-tenant project management API** built with [FastAPI](https://fastapi.tiangolo.com/).  
It provides JWT authentication, tenant-user relationships, and role-based access control for managing projects within different companies (tenants).

---

## 🚀 Features
- User registration & login with JWT authentication
- Tenant (company) creation and management
- Role-based access (admin vs normal users)
- CRUD operations for projects within a tenant
- Secure endpoints (users can only access their tenant’s data)

---

## 🛠️ Tech Stack
- **Backend:** FastAPI
- **Database:** SQLAlchemy + SQLite/PostgreSQL (configurable)
- **Auth:** JWT (OAuth2PasswordBearer)
- **Schemas:** Pydantic

---

## 📂 Project Structure
app/
├── main.py          # FastAPI entry point
├── models.py        # SQLAlchemy models (User, Tenant, Project)
├── schemas.py       # Pydantic schemas
├── routers/         # API routers (auth, users, tenants, projects)
├── database.py      # Database session setup




---

## ⚡ Quick Start

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR-USERNAME/fastapi-multi-tenant-projects.git
   cd fastapi-multi-tenant-projects
````

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Open docs:

   * Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔑 Example Endpoints

* `POST /auth/register` → Create new user
* `POST /auth/login` → Login & get JWT token
* `GET /users/profile` → Get current user profile
* `POST /tenants/create` → Create new tenant (admin only)
* `POST /projects/create` → Create project (admin only)
* `GET /projects/{tenant_id}` → List all tenant projects

---

## 📜 License

This project is licensed under the MIT License.

```



