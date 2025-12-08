# ToDo FastAPI Proof of Concept

This project is a FastAPI-based proof of concept for a to-do application that pairs user accounts with to-do entries, stores metadata in MySQL via SQLAlchemy, and exposes authentication-backed endpoints.

## Tech stack
- **FastAPI** for the web/API layer.
- **SQLAlchemy** ORM (plus core) for persistence.
- **PyJWT** for JWT-based authentication.
- **MySQL** (via `PyMySQL`) as the backing datastore.
- **Alembic** is available for migrations, and a vanilla `sessionmaker`/`declarative_base` setup powers manual queries.

## Setup
1. Create and activate a Python virtual environment (the project assumes one at `venv/`):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your MySQL credentials in `database.py` (the default points to `mysql+pymysql://root:1234@localhost/POC`).

## Database
- The ORM models live in `models/`:
  - `User` (`models/user_model.py`) stores credentials and status flags.
  - `ToDoModel` holds to-do metadata plus the `created_by` user ID.
  - `UserToDOsLink` tracks the many-to-one relation between users and to-dos.
- SQLAlchemy events in `events/todo_event.py` insert a link row after every to-do insert, keeping the join table synchronized automatically.
- Alembic is installed for migrations (`alembic.ini`), though no migrations are included yet.

## Running the API
1. Start the FastAPI app with Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
2. The API is documented via Swagger at `http://127.0.0.1:8000/docs`.
3. Routes in `user.py` include:
   - `POST /register-user`
   - `POST /login`
   - `PATCH /update-user-email` (requires Bearer JWT)
   - `DELETE /deactivate-account` (requires Bearer JWT)
4. To create a to-do, post to `/create-to-do` with a valid JWT (generated via `/login`).

## Authentication
- JWTs are encoded/decoded inside `auth.py` using a project-local secret.
- `Auth().id` is used as a dependency to inject the current user id from the `Authorization: Bearer <token>` header.

## Workflow tips
- Run `pip freeze > requirements.txt` whenever you change dependencies.
- Use the existing `events/todo_event.py` listener rather than manually syncing `UserToDOsLink`.
- Commit changes, then push them to your Git remote with `git add`, `git commit`, and `git push`.

Let me know if you want me to expand this readme with deployment instructions, testing details, or API examples. 
