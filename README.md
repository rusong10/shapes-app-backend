## Prerequisites
- Python 3.10+
- PostgreSQL
- Redis (for WebSocket functionality)

## Getting Started

Follow these steps to get your development environment set up:

**1. Clone the Repository**

  ```
  git clone <https://github.com/rusong10/shapes-app-backend.git>
  cd shapes-app-backend
  ```

**2. Create and Activate a Virtual Environment**
- Windows:
  
  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```
- macOS/Linux:
  ```
  python -m venv venv
  source venv/bin/activate
  ```

**3. Install Dependencies**

  ```
  pip install -r requirements.txt
  ```

**4. Set Up Environment Variables**

This project uses `django-environ` to manage envrionment settings. Create a .env file in the project root:
  
```
DEBUG=True
ENV=development # Or 'production', 'staging', etc.
SECRET_KEY=your_secret_key

# Database
DB_NAME=shapes_dev_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,api.localtest.me

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://app.localtest.me:3000

# CSRF
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://app.localtest.me:3000
  
# SimpleJWT
ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=30

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```
> **_NOTE:_** The `shapes_app_backend/settings.py` file is configured to load environment variables from `.env`. You can modify this path if needed.

**5. Set Up PostgreSQL Database**

1. Ensure your PostgreSQL server is running.
   
2. Create the database specified in your `.env` file:
   
    ```
    CREATE DATABASE shapes_dev_db;
    CREATE USER your_user WITH PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE shapes_dev_db TO your_user;
    ```
3. You can use tools like `pgAdmin 4` or `psql` to manage your database

**6. Set up Redis (requried for WebScoket communication)**

- Windows (using WSL) or Linux:
  
  ```
  sudo apt update && sudo apt upgrade
  sudo apt install redis-server
  sudo systemctl start redis-server
  ```

- macOS:

  ```
  brew install redis
  brew services start redis
  ```
  
- Verify Redis is running::
  
  ```
  redis-cli ping
  ```
  You should receive `PONG` as a response.

**6. Apply Database Migrations**

  This will create the necessary tables in your database based on the Django models.
  
  ```
  python manage.py makemigrations accounts
  python manage.py makemigrations shapes
  python manage.py migrate
  ```

**7. Create a Superuser (Admin Account)**
  - This account will have full permissions to manage shapes via the API. Follow the prompts to set a username, email (optional), and password.
    
    ```
    python manage.py createsuperuser
    ```

**8. Run the server**
  - Ensure Redis is running (if configured in `shapes_app_backend/settings.py` under `CHANNEL_LAYERS`)
  - Run the Django ASGI server:
      
    ```
    python manage.py runserver app.localtest.me:8000
    ```
    > **_NOTE:_** We use `app.localtest.me` instead of `localhost` so cookies (especially with `SameSite=Lax`) work correctly across subdomains, just like in production.

## API Endpoints

All API endpoints are prefixed with `/api/`.
- Authentication (/api/auth/)
  - `POST /api/accounts/login/:` User login. Returns access token, user info and sets refresh token cookie.
  - `POST /api/accounts/logout/:` User logout. Blacklists refresh token.
  - `POST /api/accounts/token/refresh/`: Refresh access token using the refresh_token cookie.
  - `POST /api/accounts/token/verify/`: Verify an access token.
  - `POST /api/accounts/me/`: Get current user information

- Shapes (/api/shapes/)
   - `GET /api/shapes/:` List all shapes (Publicly accessible).
   - `POST /api/shapes/:` Create a new shape (Admin only).
   - `GET /api/shapes/{id}/`: Retrieve a specific shape (Publicly accessible).
   - `PUT /api/shapes/{id}/`: Update a specific shape (Admin only).
   - `PATCH /api/shapes/{id}/`: Partially update a specific shape (Admin only).
   - `DELETE /api/shapes/{id}/`: Delete a specific shape (Admin only).
 
## WebSocket Endpoints
- `/ws/shapes/` Real-time shape updates

## Authentication Flow
1. Login: POST to `/api/accounts/login/` with username and password
2. Using the Token: Add the access token to the Authorization header for protected endpoints:

   ```
   Authorization: Bearer <access_token>
   ```
3. Token Refresh: When the access token expires, the client can get a new one by sending a POST request to `/api/accounts/token/refresh/`
