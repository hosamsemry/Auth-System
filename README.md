# Simple Auth System

This is a RESTful API for user authentication (no third party packages). The system provides secure endpoints for user registration, login, and token management.

## Available Endpoints so far

#### 1. Register a New User
- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "username": "newuser",
    "password": "securepassword123",
    "password2": "securepassword123"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "newuser"
    },
    "token": {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
  }
  ```

#### 2. Login
- **URL**: `/api/accounts/login/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "password": "securepassword123"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "newuser"
    },
    "token": {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
  }
  ```

#### 3. Refresh Token
- **URL**: `/api/accounts/refresh/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "access": "new_access_token_here"
  }
  ```

#### 4. Get Current User
- **URL**: `/api/accounts/me/`
- **Method**: `GET`
- **Headers**:
  ```
  Authorization: Token <access_token>
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "newuser"
  }
  ```

#### 5. Forgot Password
- **URL**: `/api/accounts/forgot-password/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Password reset code has been sent to your email"
  }
  ```

#### 6. Reset Password
- **URL**: `/api/accounts/reset-password/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "code": "reset_code_from_email",
    "new_password": "new_secure_password"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Password reset successful"
  }
  ```

#### 7. Logout
- **URL**: `/api/accounts/logout/`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: Token <access_token>
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Successfully logged out"
  }
  ```

## 🔧 Technologies Used

- **Backend Framework**: Django 4.2+
- **REST API**: Django REST Framework
- **Authentication**: Custom Token Authentication
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Task Queue**: Celery (for async email sending)
- **Environment Management**: python-dotenv
