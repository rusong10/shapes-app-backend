## Getting Started

Follow these steps to get your development environment set up:

**1. Clone the Repository**

```
git clone <https://github.com/rusong10/shapes-app-backend.git>
cd shapes-app-backend
```

**2. Create and Activate a Virtual Environment**
- Windows (Command Prompt):
```
python -m venv .venv
.venv\Scripts\activate
```

**3. Install Dependencies**
```
pip install -r requirements.txt
```

**4. Set Up Environment Variables**

You can copy the template below into a new file named .env (or .env.dev, .env.prod etc.).
```
DEBUG=True
ENV=your_dev_environment
SECRET_KEY=your_secret_key

# Database
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# CSRF
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# SimpleJWT
ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=1
```
- The `settings.py` file is configured to load environment variables from `.env.dev`, you may change to your env file accordingly. (line 24)

**5. Set Up PostgreSQL Database**
- Ensure your PostgreSQL server is running.
- Create the database specified in your .env file (e.g., shapes_dev_db) with the specified user and password having ownership or appropriate permissions via `pgAdmin 4` or `psql`.

**6. Apply Database Migrations**

This will create the necessary tables in your database based on the Django models.
```
python manage.py makemigrations accounts
python manage.py makemigrations shapes_app
python manage.py migrate
```

**7. Create a Superuser (Admin Account)**
- This account will have full permissions to manage shapes via the API. Follow the prompts to set a username, email (optional), and password.
```
python manage.py createsuperuser
```

**8. Run the server**
```
python manage.py runserver localhost:8000
```

## API Endpoints Overview

All API endpoints are prefixed with `/api/`.
- Authentication (/api/auth/)
  - `POST /api/auth/login/:` User login. Returns access token, username, and sets refresh token cookie.
  - `POST /api/auth/logout/:` User logout. Blacklists refresh token. Requires Authorization header and X-CSRFToken header.
  - `POST /api/auth/token/refresh/`: Refresh access token using the refresh_token cookie. Requires X-CSRFToken header.
  - `POST /api/auth/token/verify/`: Verify an access token.

- Shapes (/api/shapes/)
   - `GET /api/shapes/:` List all shapes (Publicly accessible).
   - `POST /api/shapes/:` Create a new shape (Admin only, requires Authorization).
   - `GET /api/shapes/{id}/`: Retrieve a specific shape (Publicly accessible).
   - `PUT /api/shapes/{id}/`: Update a specific shape (Admin only, requires Authorization).
   - `PATCH /api/shapes/{id}/`: Partially update a specific shape (Admin only, requires Authorization).
   - `DELETE /api/shapes/{id}/`: Delete a specific shape (Admin only, requires Authorization).
