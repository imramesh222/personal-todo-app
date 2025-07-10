# FastAPI To-Do App

A modern To-Do application built with FastAPI, supporting JWT authentication, user/admin roles, and PostgreSQL.

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd todo_app
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/todoapp
SECRET_KEY=your_secret_key
SERVICE_PORT=8004
```
Adjust values as needed.

### 5. Set Up the Database
- Ensure PostgreSQL is running and the `todoapp` database exists.
- Run Liquibase migrations:
```bash
cd liquibase
liquibase update
cd ..
```

### 6. Start the Application
```bash
./start_service.sh
```
The app will run on the port specified by `SERVICE_PORT` (default: 8000).

### 7. Access the API Docs
- Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## 🔑 Authentication & Roles
- **JWT-based authentication**: Register and log in to receive a token.
- **Roles**: `user` (default) or `admin`.
  - Register as admin by including `"role": "admin"` in the registration payload.
  - Admins can manage all users and todos; users can only manage their own data.

---
---

## 🔐 OAuth2PasswordBearer Login Flow

This app uses FastAPI's `OAuth2PasswordBearer` for secure login:
- **Token URL:** `/auth/token`
- **Flow:** password (username = email, password = your password)

**How to log in using Swagger UI:**
1. Go to [http://0.0.0.0:8004][http://localhost:8000/docs]
2. Click the "Authorize" button (top right).
3. Enter your email as the username and your password.
4. Click "Authorize" to obtain a Bearer token for testing protected endpoints.

---

## 📚 API Endpoint Usage

### User Endpoints

- **Register**
  - `POST /users/`
  - **Request JSON:**
    ```json
    {
      "full_name": "Ramesh Rawat",
      "email": "ramesh@gmail.com",
      "password": "yourpassword",
      "role": "admin"  // optional, default is "user"
    }
    ```

- **Login**
  - `POST /auth/token`
  - **Form Data:**
    - `username`: your email
    - `password`: your password
  - **Response:** `{ "access_token": "...", "token_type": "bearer" }`

- **Get Current User**
  - `GET /users/me` (requires Bearer token)

- **Update User**
  - `PUT /users/{user_id}` (admin can update any user, normal user can update self)

- **Delete User**
  - `DELETE /users/{user_id}` (admin can delete any user, normal user can delete self)

- **List All Users**
  - `GET /users/` (admin only)

---

### To-Do Endpoints

- **List To-Dos**
  - `GET /todos/` (admin: all todos, user: own todos)

- **Create To-Do**
  - `POST /todos/`
  - **Request JSON:**
    ```json
    {
      "task": "Buy groceries"
    }
    ```

- **Update To-Do**
  - `PUT /todos/{todo_id}` (admin: any todo, user: own todo)

- **Delete To-Do**
  - `DELETE /todos/{todo_id}` (admin: any todo, user: own todo)

---

## 🛡️ Notes
- All endpoints (except registration and login) require a valid Bearer token.
- Only admins can list all users or all todos.
- Passwords are securely hashed.
- After deleting your own user, your token becomes invalid (log out).

---

## 🧑‍💻 Development
- See `.gitignore` for ignored files.
- Use the provided Liquibase migrations for DB schema management.

---

## 📫 Contact
For questions or contributions, open an issue or pull request.



## 🖼️ Screenshots

You can add screenshots of request/response testing in Swagger UI to your README for better documentation.

Example:
```markdown
## Example: Logging in via Swagger UI
[Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.19.20.png)!
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.19.36.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.20.09.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.20.23.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.20.37.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.21.02.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.21.14.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.21.26.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.21.52.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.22.02.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.22.15.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.22.29.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.22.43.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.22.57.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.23.08.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.23.21.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.23.33.png)
![Test Results](docs/screenshots/Screenshot%202025-07-10%20at%2017.23.51.png)

```


---
