# 💰 Personal Finance Tracker Backend

A comprehensive Django REST API backend for a personal finance tracking application. This project helps users manage their income, expenses, budgets, and financial habits through an intuitive dashboard and APIs.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

**Smart Personal Finance Tracker** is an assignment project designed to help users track their financial activities. The backend provides RESTful APIs for user authentication, transaction management, expense categorization, budget tracking, and automated bill reminders.

**Current Status:** ✅ Core features implemented and documented

---

## ✨ Features Implemented

### 1️⃣ **User Authentication System**
- ✅ User registration with email validation
- ✅ JWT-based authentication (Access & Refresh tokens)
- ✅ User login/logout
- ✅ Password hashing with Django's built-in security
- ✅ User profile management
- ✅ Password reset with OTP (6-digit code)
- ✅ Change password functionality
- ✅ Token validation and refresh

### 2️⃣ **Transaction Management**
- ✅ Create, read, update, delete transactions
- ✅ Support for income and expense types
- ✅ Category-based organization
- ✅ Transaction descriptions and dates
- ✅ User-specific transaction filtering
- ✅ Transaction history with ordering

### 3️⃣ **Category Management**
- ✅ Create custom categories
- ✅ Edit and delete categories
- ✅ Category types: Income & Expense
- ✅ User-specific categories
- ✅ Duplicate category prevention

### 4️⃣ **Dashboard Analytics**
- ✅ Total income calculation
- ✅ Total expense calculation
- ✅ Balance summary
- ✅ Monthly spending trends
- ✅ Category-wise expense distribution
- ✅ Pending and overdue reminders tracking

### 5️⃣ **Bill & Payment Reminders**
- ✅ Create payment reminders
- ✅ Set reminder notifications (days before due date)
- ✅ Automated email notifications
- ✅ Background job scheduler (APScheduler)
- ✅ Mark reminders as completed
- ✅ Update and delete reminders
- ✅ Email templates for notifications

### 6️⃣ **Security Features**
- ✅ Password hashing (PBKDF2 with SHA256)
- ✅ JWT token authentication
- ✅ User-specific data isolation
- ✅ Input validation (serializers)
- ✅ CORS configuration
- ✅ OTP-based password reset

---

## 🛠 Tech Stack

### Backend
- **Framework:** Django 6.0.1
- **REST API:** Django REST Framework 3.16.1
- **Authentication:** JWT (djangorestframework-simplejwt 5.5.1)
- **Database:** PostgreSQL (psycopg2-binary 2.9.11)
- **Task Scheduling:** APScheduler (django_apscheduler 0.7.0)
- **Email:** Django Mail
- **CORS:** django-cors-headers 4.9.0
- **Server:** Gunicorn 25.0.0
- **Testing:** Django unittest, Coverage 7.13.5

### Development Tools
- Python 3.x
- Pip (package manager)
- Git (version control)
- environment variables (.env)

---
---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd personal-finance-tracker-backend
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
Create a `.env` file in the project root:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/finance_tracker_db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# JWT Settings
JWT_SECRET=your-jwt-secret-key

---

## ⚙️ Configuration

### Django Settings (`core/settings.py`)
- **DEBUG:** Set to `False` in production
- **ALLOWED_HOSTS:** Configure for your domain
- **INSTALLED_APPS:** All Django apps registered
- **REST_FRAMEWORK:** Custom pagination, authentication, renderers
- **CORS_ALLOWED_ORIGINS:** Configure frontend URLs

### Email Configuration
The app uses Gmail SMTP for sending OTP and reminder emails:
1. Enable 2-factor authentication on your Gmail account
2. Generate an app-specific password
3. Use that password in `EMAIL_HOST_PASSWORD`

### JWT Configuration
Tokens are configured in `settings.py`:
- **Access Token Expiry:** 60 minutes
- **Refresh Token Expiry:** 7 days

---

## ▶️ Running the Server

### Development Server
```bash
python manage.py runserver
```
Server runs at `http://127.0.0.1:8000/`


### Production Server (Gunicorn)
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

---

## 📡 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | User login & get tokens |
| GET | `/api/auth/profile/` | Get user profile |
| PUT | `/api/auth/profile/` | Update user profile |
| POST | `/api/auth/change-password/` | Change password |
| POST | `/api/auth/request-otp/` | Request password reset OTP |
| POST | `/api/auth/confirm-otp/` | Reset password using OTP |
| POST | `/api/auth/validate-token/` | Validate/refresh JWT tokens |

### Transaction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions/` | List all transactions |
| POST | `/api/transactions/` | Create new transaction |
| GET | `/api/transactions/{id}/` | Get transaction details |
| PUT | `/api/transactions/{id}/` | Update transaction |
| DELETE | `/api/transactions/{id}/` | Delete transaction |

### Category Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/category/` | List all categories |
| POST | `/api/category/` | Create new category |
| PUT | `/api/category/{id}/` | Update category |
| DELETE | `/api/category/{id}/` | Delete category |

### Reminder Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reminders/` | List all reminders |
| POST | `/api/reminders/` | Create reminder |
| PUT | `/api/reminders/{id}/` | Update reminder |
| PATCH | `/api/reminders/{id}/action/` | Mark reminder as read/completed |
| DELETE | `/api/reminders/{id}/` | Delete reminder |

### Dashboard Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/` | Get dashboard summary (income, expense, trends) |

---

## 💾 Database Schema

### Users Table
```sql
-- Extended User Profile
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES auth_user(id),
    phone VARCHAR(20),
    currency VARCHAR(10) DEFAULT 'EUR',
    created_at TIMESTAMP
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES auth_user(id),
    category_id INT REFERENCES categories(id),
    amount DECIMAL(12, 2),
    type VARCHAR(20), -- 'income' or 'expense'
    description TEXT,
    date DATE,
    created_at TIMESTAMP
);
```

### Categories Table
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES auth_user(id),
    name VARCHAR(100),
    type VARCHAR(20), -- 'income' or 'expense'
    created_at TIMESTAMP
);
```

### Reminders Table
```sql
CREATE TABLE reminders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES auth_user(id),
    title VARCHAR(150),
    amount DECIMAL(12, 2),
    due_date DATE,
    reminder_days_before INT,
    is_completed BOOLEAN DEFAULT FALSE,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP
);
```

### OTP Table
```sql
CREATE TABLE password_reset_otp (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES auth_user(id),
    otp VARCHAR(6),
    created_at TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE
);
```

---

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Tests with Coverage Report
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML report in htmlcov/
```

## 🌐 Deployment

### Deploy to Railway
1. Push code to GitHub
2. Connect repository to Railway
3. Set environment variables in Railway dashboard
4. Configure PostgreSQL database
5. Deploy and generate Railway URL

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=generate-strong-key
DATABASE_URL=postgresql://user:password@host:port/dbname
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-specific-password
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Pre-Deployment Checklist
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Configure database URL
- [ ] Set up HTTPS
- [ ] Configure CORS properly
- [ ] Test all API endpoints
- [ ] Enable logging
- [ ] Configure email service

---


## 📝 API Response Format

### Success Response
```json
{
    "isSuccess": true,
    "message": "Operation successful",
    "data": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

### Error Response
```json
{
    "isSuccess": false,
    "message": "Error description",
    "data": null
}
```

---

## 🚀 Quick Start Command Reference

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Environment
# Create .env file with required variables

# Database
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver

# Test
python manage.py test
coverage run --source='.' manage.py test

# Production
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

---