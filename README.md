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
  .\venv\Scripts\activate
  ```

**3. Install Dependencies**

  ```
  pip install -r requirements.txt
  ```

**4. Set Up Environment Variables**

This project uses `django-environ` to manage env settings. You will need to create an environment file (e.g., `.env` or `.env.dev`) in the root of the project.
- Create your environment files:
  
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
  ALLOWED_HOSTS=localhost,127.0.0.1
  
  # CORS
  CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
  
  # CSRF
  CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
  
  # SimpleJWT
  ACCESS_TOKEN_LIFETIME_MINUTES=15
  REFRESH_TOKEN_LIFETIME_DAYS=1

  # Redis
  REDIS_HOST=127.0.0.1
  REDIS_PORT=6379
  ```
- The `shapes_app_backend/settings.py` file is configured to load environment variables from `.env.dev`, you may change to your env file accordingly. (line 24)

**5. Set Up PostgreSQL Database**

- Ensure your PostgreSQL server is running.
- Create the database specified in your .env file (e.g., shapes_dev_db)
- Ensure the specified user `(POSTGRES_USER)` has the necessary permissions for this database. Use tools like `pgAdmin 4` or `psql`.

**6. Set up Redis (requried for WebScoket communication)**

- For Windows, use WSL to install a Linux distribution like Ubuntu, then run the following command
  
  ```
  sudo apt update && sudo apt upgrade
  sudo apt install redis
  sudo service redis-server start
  ```
- Verify if Redis is Running by using the Redis CLI:
  
  ```
  redis-cli ping
  ```
  It should respond with `PONG`.

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
  - Ensure Redis is running (if configured in `shapes_app_backend/settings.py` under `CHANNEL_LAYERS`)
  - Run the Django ASGI server:
      
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
