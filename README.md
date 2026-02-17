<div align=center>

# Business Dashboard

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

A production-ready customer and order management system built with Flask and SQLAlchemy. Multi-user support, role-based data isolation, password reset via email, and a clean dashboard interface.

---
</div>

## Description

Business Dashboard is a CRUD app I built because I needed something simple to manage customers and orders without the bloat of enterprise software. Most business management tools are either too complex (Salesforce, anyone?) or too simplistic (glorified spreadsheets). I wanted something in between: a straightforward web interface with user accounts, email notifications, and actual data validation.

The app handles the basics well: create customers, track orders, see your revenue at a glance. Each user's data is completely isolated—you only see your own customers and orders. Pagination works, forms validate properly, and password resets actually send emails instead of just logging to console.

Built this to understand Flask blueprints, SQLAlchemy relationships, and how to structure a multi-user app without making a mess. It's not trying to be Shopify, but it works reliably for small businesses or freelancers who need to track client work.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Key Routes](#key-routes)
- [Security Features](#security-features)
- [Architecture Decisions](#architecture-decisions)
- [Production Deployment](#production-deployment)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [What I Learned](#what-i-learned)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd business-dashboard
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Setup environment variables (create .env file)
cat > .env << EOF
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL=sqlite:///instance/business.db
FLASK_ENV=development
MAIL_SERVER=smtp.gmail.com
BUSINESS_DASHBOARD_EMAIL=your-email@gmail.com
BUSINESS_DASHBOARD_EMAIL_PASSWORD=your-app-password
EOF

# Initialize database
flask db upgrade

# Run the app
python run.py
# Visit http://localhost:5000
```

---

## Features

- ✅ **Multi-user authentication** – Each user has isolated customer/order data
- ✅ **Customer management** – Full CRUD with email validation
- ✅ **Order tracking** – Link orders to customers, track status and revenue
- ✅ **Dashboard stats** – Total customers, orders, pending orders, and revenue at a glance
- ✅ **Password reset via email** – Secure token-based recovery (1-hour expiry)
- ✅ **Pagination** – Handle large datasets without breaking the UI
- ✅ **Form validation** – WTForms with custom validators (duplicate email checks, order number conflicts)
- ✅ **Data isolation** – Users can only access their own data (enforced at the query level)
- ✅ **Foreign key protection** – Can't delete customers who have existing orders
- ✅ **Responsive design** – Works on mobile and desktop

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Python, Flask | Web framework |
| **Database** | SQLAlchemy, SQLite | ORM and persistent storage |
| **Migrations** | Flask-Migrate (Alembic) | Database schema versioning |
| **Forms** | Flask-WTF, WTForms | Form handling and CSRF protection |
| **Authentication** | Werkzeug, itsdangerous | Password hashing, secure tokens |
| **Email** | Flask-Mail | Password reset emails |
| **Frontend** | Jinja2, Bootstrap | Templates and styling |

### Why This Stack?

**Flask** – Lightweight, flexible, doesn't impose architecture decisions  
**SQLAlchemy** – Powerful ORM with relationship handling and migrations  
**WTForms** – Server-side validation with reusable form classes  
**SQLite** – Zero-config database perfect for small-to-medium deployments  
**Flask-Migrate** – Handles schema changes without manual SQL

This is a classic Flask stack that prioritizes simplicity and maintainability over bleeding-edge features.

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- Git
- SMTP server access (Gmail works out of the box)

### Step 1: Clone and Setup Virtual Environment
```bash
git clone <repository-url>
cd business-dashboard

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:
```bash
SECRET_KEY=your-secret-key-here  # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
DATABASE_URL=sqlite:///instance/business.db
FLASK_ENV=development

# Email configuration (required for password resets)
MAIL_SERVER=smtp.gmail.com
BUSINESS_DASHBOARD_EMAIL=your-email@gmail.com
BUSINESS_DASHBOARD_EMAIL_PASSWORD=your-gmail-app-password  # NOT your regular password
```

**Getting a Gmail App Password:**
1. Enable 2FA on your Google account
2. Go to Google Account → Security → 2-Step Verification → App passwords
3. Generate a new app password for "Mail"
4. Use that 16-character password in your `.env` file

**Config validation:** The app validates required email variables on startup and prints missing ones to help with troubleshooting.

### Step 4: Initialize Database
```bash
# Create migration folder (first time only)
flask db init

# Run migrations
flask db upgrade
```

This creates the SQLite database file with the correct schema.

### Step 5: Run the Application

**Development mode:**
```bash
python run.py
# Visit http://localhost:5000
```

**Production mode:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
# Visit http://localhost:8000
```

---

## Configuration

All configuration lives in `app/config.py` and pulls from environment variables.

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | Flask session encryption key (64 chars recommended) |
| `DATABASE_URL` | Yes | `sqlite:///dev.db` | Database connection string |
| `FLASK_ENV` | No | `production` | Set to `development` to enable debug mode |
| `MAIL_SERVER` | Yes | - | SMTP server address (e.g., `smtp.gmail.com`) |
| `BUSINESS_DASHBOARD_EMAIL` | Yes | - | Email address for sending |
| `BUSINESS_DASHBOARD_EMAIL_PASSWORD` | Yes | - | Email password or app-specific password |

### Configuration Classes

The app uses different configs for development and production:

**DevelopmentConfig:**
- Debug mode enabled
- Auto-reload on code changes
- Detailed error pages
- Uses SQLite with default path: `sqlite:///dev.db`

**ProductionConfig:**
- Debug mode disabled
- Generic error pages
- Requires `DATABASE_URL` environment variable
- Can use PostgreSQL or MySQL via `DATABASE_URL`
- Secure session cookies

Switch between them by setting `FLASK_ENV`:
```bash
export FLASK_ENV=development  # or production
```

### Config Structure

All configuration inherits from a base `Config` class in `app/config.py`:
```python
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("BUSINESS_DASHBOARD_EMAIL")
    MAIL_PASSWORD = os.environ.get("BUSINESS_DASHBOARD_EMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Business Dashboard", MAIL_USERNAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

**Startup validation:** On import, the config checks for missing required variables and prints warnings:
```python
for name in ["MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_DEFAULT_SENDER", "MAIL_SERVER"]:
    if getattr(Config, name) is None:
        print(f"Missing: {name}")
```

This helps catch configuration errors early instead of failing silently later.

---

## Usage

### Creating an Account

1. Visit the homepage and click **"Sign Up"**
2. Enter your name, email, and password
3. Password requirements:
   - At least 6 characters
   - At least 1 letter
   - At least 1 number
   - At least 1 special character
4. Click **"Sign Up"** – you'll be automatically logged in

### Adding Customers

1. Log in and click **"Customers"** → **"Add Customer"**
2. Fill in the form:
   - **Name:** Customer's full name
   - **Email:** Valid email address (must be unique)
   - **Phone:** Optional phone number
   - **Company:** Optional company name
3. Click **"Save Customer"**

**Note:** Email addresses must be unique across all customers in your account.

### Creating Orders

1. Click **"Orders"** → **"Add Order"**
2. Fill in the form:
   - **Order ID:** Unique order number (e.g., `ORD-001`)
   - **Customer:** Select from your existing customers
   - **Product:** Product or service name
   - **Quantity:** Number of units
   - **Price:** Unit price (not total)
   - **Status:** Pending, Processing, Completed, or Cancelled
3. Click **"Save Order"**

**Important:** You must have at least one customer before creating orders. The app will prompt you if you try to create orders without customers.

### Dashboard Overview

The main dashboard shows four key metrics:

| Metric | Description |
|--------|-------------|
| **Total Customers** | Count of all your customers |
| **Total Orders** | Count of all orders across all customers |
| **Pending Orders** | Orders with "pending" status |
| **Total Revenue** | Sum of (quantity × price) for all orders |

### Editing and Deleting

**To edit a customer or order:**
1. Go to Customers or Orders page
2. Click the **Edit** button next to the entry
3. Update the form and click **"Update"**

**To delete:**
1. Click the **Delete** button next to the entry
2. Confirm deletion

**Protection:** You cannot delete a customer who has existing orders. Delete the orders first.

### Password Reset

1. Click **"Forgot Password?"** on the login page
2. Enter your email address
3. Check your email for a reset link (valid for 1 hour)
4. Click the link and enter your new password
5. You'll be redirected to login

**Security note:** The app always shows "email sent" even if the address isn't registered (prevents email enumeration attacks).

---

## Project Structure
```
business-dashboard/
│
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration classes (Dev/Prod)
│   ├── extensions.py            # Flask extensions (db, mail, migrate)
│   ├── mail_utils.py            # Email sending utilities
│   │
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py         # Blueprint registration
│   │   ├── routes.py           # Login, signup, password reset routes
│   │   ├── decorators.py       # @login_required decorator
│   │   └── utils.py            # current_user() helper
│   │
│   ├── models/                  # Database models
│   │   ├── __init__.py         # Model imports + password helpers
│   │   ├── user.py             # User model + hash_password/validate_password
│   │   ├── customer.py         # Customer model
│   │   └── order.py            # Order model with total_amount property
│   │
│   ├── forms/                   # WTForms form classes
│   │   ├── __init__.py         # Form imports
│   │   ├── auth_forms.py       # SignUp, Login, ForgotPassword, ResetPassword
│   │   ├── customer.py         # CustomerCreate, CustomerEdit (with BaseForm)
│   │   └── order.py            # OrderCreate, OrderEdit (with BaseForm)
│   │
│   ├── routes/                  # Route blueprints
│   │   ├── __init__.py         # Blueprint registration helper
│   │   ├── main.py             # Dashboard homepage (index_bp)
│   │   ├── customers.py        # Customer CRUD routes (customers_bp)
│   │   └── orders.py           # Order CRUD routes (orders_bp)
│   │
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── layout.html         # Base template with navbar
│   │   ├── macros.html         # Reusable template macros
│   │   ├── index.html          # Dashboard page
│   │   ├── customers.html      # Customer list with pagination
│   │   ├── customer_form.html  # Customer create/edit form
│   │   ├── orders.html         # Order list with pagination
│   │   ├── order_form.html     # Order create/edit form
│   │   │
│   │   └── auth/               # Authentication templates
│   │       ├── signup.html
│   │       ├── login.html
│   │       ├── forgot_password.html
│   │       ├── reset_password.html
│   │       ├── reset_email.html      # HTML email template
│   │       └── reset_email.txt       # Plain text email template
│   │
│   └── static/                  # Static assets
│       ├── css/
│       ├── js/
│       └── favicon/
│           ├── logo.png
│           └── plogo.svg
│
├── instance/                    # Instance-specific files
│   └── business.db             # SQLite database (auto-generated)
│
├── migrations/                  # Alembic migration files
│   ├── versions/               # Individual migration scripts
│   ├── alembic.ini
│   └── env.py
│
├── venv/                       # Virtual environment (gitignored)
│
├── run.py                      # Application entry point (includes before_request hooks)
├── gunicorn.conf.py            # Gunicorn production configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (gitignored)
└── README.md                   # This file
```

---

## Database Schema

The app uses three main tables with foreign key relationships:

### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

**Password helper functions:** The `models/user.py` file also exports:
```python
def hash_password(password):
    return generate_password_hash(password)

def validate_password(user_password, password):
    return check_password_hash(user_password, password)
```

These live alongside the `User` model to keep authentication logic centralized.

### customer
```sql
CREATE TABLE customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### order
```sql
CREATE TABLE "order" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    product VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    price FLOAT NOT NULL DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'pending',
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);
```

**Property-based computed field:**

The `Order` model includes a `@property` for calculated total:
```python
@property
def total_amount(self):
    return self.quantity * self.price
```

This means you can access `order.total_amount` without storing it in the database. It's always computed on-the-fly, ensuring consistency.

### Relationships

**One-to-Many:**
- User → Customers (one user has many customers)
- Customer → Orders (one customer has many orders)

**Key Constraints:**
- User emails must be unique globally
- Customer emails must be unique globally
- Order numbers must be unique per user (enforced in forms)
- Cannot delete customers with existing orders (enforced in routes)

### Querying Patterns

**Get user's customers:**
```python
customers = Customer.query.filter_by(user_id=current_user.id).all()
```

**Get user's orders (with join):**
```python
orders = Order.query.join(Customer).filter(Customer.user_id == current_user.id).all()
```

**Calculate total revenue:**
```python
revenue = sum(order.price * order.quantity for order in orders)
```

### Application Entry Point

The `run.py` file handles application initialization and user loading:

```python
from app.extensions import db
from flask import g, session
from app.models import *
from app import create_app

app = create_app()

@app.before_request
def activate_current_user():
    """Load current user before each request"""
    user_id = session.get("user_id")
    g.user = db.session.get(User, user_id) if user_id else None

@app.context_processor
def inject_user():
    """Make current_user available in all templates"""
    return dict(current_user=g.user)

if __name__ == "__main__":
    app.run(debug=True)
```

**How this works:**

1. **`@app.before_request`** runs before every route handler
2. Checks for `user_id` in session
3. If found, loads the `User` object and stores it in `g.user`
4. If not found, `g.user` is `None` (anonymous user)
5. **`@app.context_processor`** makes `current_user` available in templates
6. Routes can access `g.user` directly without repeated database queries

This pattern ensures the current user is always available where needed without manually loading it in every route.

---

## Key Routes

### Public Routes (no login required)

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/signup` | Registration page |
| `POST` | `/signup` | Process registration form |
| `GET` | `/login` | Login page |
| `POST` | `/login` | Process login form |
| `GET` | `/forgot_password` | Password reset request page |
| `POST` | `/forgot_password` | Send password reset email |
| `GET` | `/reset_password/<token>` | Password reset form |
| `POST` | `/reset_password/<token>` | Update password |

### Protected Routes (login required)

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Dashboard with stats |
| `POST` | `/logout` | Clear session and log out |

**Customers:**

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/customers` | List all customers (paginated) |
| `GET` | `/customers/new` | Customer creation form |
| `POST` | `/customers/new` | Save new customer |
| `GET` | `/customers/<id>/edit` | Customer edit form |
| `POST` | `/customers/<id>/edit` | Update customer |
| `POST` | `/customers/<id>/delete` | Delete customer |

**Orders:**

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/orders` | List all orders (paginated) |
| `GET` | `/orders/new` | Order creation form |
| `POST` | `/orders/new` | Save new order |
| `GET` | `/orders/<id>/edit` | Order edit form |
| `POST` | `/orders/<id>/edit` | Update order |
| `POST` | `/orders/<id>/delete` | Delete order |

---

## Security Features

- ✅ **Password hashing** – Werkzeug's `generate_password_hash` with salt
- ✅ **CSRF protection** – Flask-WTF on all forms
- ✅ **Secure password reset** – Time-limited tokens (1 hour) using `itsdangerous`
- ✅ **User enumeration prevention** – Password reset always shows "email sent"
- ✅ **Data isolation** – Users can only access their own data via query filters
- ✅ **SQL injection protection** – SQLAlchemy parameterized queries
- ✅ **XSS protection** – Jinja2 auto-escapes all variables
- ✅ **Password complexity** – Enforced via regex validators
- ✅ **Email validation** – WTForms Email validator
- ✅ **Unique constraints** – Prevent duplicate emails and order numbers
- ✅ **Foreign key checks** – Prevent orphaned records

### How Data Isolation Works

Every query for customers or orders includes the `user_id` filter:

**Customers route:**
```python
customers = Customer.query.filter_by(user_id=user.id).all()
```

**Orders route (with join):**
```python
orders = Order.query.join(Customer).filter(Customer.user_id == user.id).all()
```

**Edit/delete routes:**
```python
customer = Customer.query.filter(
    Customer.id == id, 
    Customer.user_id == user.id
).first_or_404()
```

This ensures User A can never access User B's data, even if they guess the ID.

### Password Reset Flow

1. User enters email → Backend checks if user exists
2. If user exists: Generate time-limited token (1 hour), send email
3. If user doesn't exist: Show "email sent" anyway (prevents enumeration)
4. User clicks link → Token validated (signature + expiry)
5. Invalid/expired token → Error page
6. Valid token → Password reset form
7. Password updated → Redirect to login

Token generation:
```python
s = URLSafeTimedSerializer(app.secret_key)
token = s.dumps(user.id, salt="password-reset-salt")
```

Token validation:
```python
try:
    id = s.loads(token, salt="password-reset-salt", max_age=3600)
except (BadSignature, SignatureExpired):
    # Invalid or expired
```

---

## Architecture Decisions

### Blueprint Organization

The app uses Flask blueprints to separate concerns:

**`auth` blueprint** – All authentication-related routes  
**`index` blueprint** – Dashboard homepage  
**`customers` blueprint** – Customer CRUD  
**`orders` blueprint** – Order CRUD

**Benefits:**
- Routes are organized by feature, not in one giant file
- Each blueprint can have its own templates folder
- URL prefixes are defined once per blueprint (`/customers`, `/orders`)
- Easy to test individual blueprints in isolation

### Form Validation Strategy

Forms inherit from base classes to avoid duplication:

**Customer forms:**
```python
class BaseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Length(max=20)])
    company = StringField('Company', validators=[Length(max=100)])

class CustomerCreate(BaseForm):
    submit = SubmitField('Save Customer')
    
    def validate_email(self, email):
        # Check if email already exists
        customer = Customer.query.filter_by(email=email.data).first()
        if customer:
            raise ValidationError("Email is connected to another customer")

class CustomerEdit(BaseForm):
    submit = SubmitField('Update Customer')
    
    def __init__(self, customer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer
    
    def validate_email(self, email):
        # Check if email exists for a different customer
        customer = Customer.query.filter(
            Customer.email == email.data, 
            self.customer.id != Customer.id
        ).first()
        if customer:
            raise ValidationError('Email is connected to another customer')
```

**Why this works:**
- `CustomerCreate` checks for any duplicate email
- `CustomerEdit` checks for duplicate email excluding the current customer
- Shared fields defined once in `BaseForm`
- Custom validators use WTForms' built-in validation flow

### Order Number Uniqueness Per User

Order numbers must be unique per user (not globally):

```python
def validate_order_number(self, order_number):
    order = Order.query.join(Customer).filter(
        Order.order_number == order_number.data,
        Customer.user_id == self.user_id
    ).first()
    
    if order:
        raise ValidationError('Order number already registered.')
```

This allows different users to use the same order number scheme (e.g., "ORD-001") without conflicts.

### Dynamic Form Choices

Order forms need to show only the current user's customers in the dropdown:

```python
class BaseForm(FlaskForm):
    customer_id = SelectField('Customer ID', coerce=int, validators=[DataRequired()])
    # ... other fields ...
    
    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        
        if user_id:
            self.customer_id.choices = [
                (c.id, c.name) 
                for c in Customer.query.filter(Customer.user_id == user_id).all()
            ]
        else:
            self.customer_id.choices = []
```

**Why this works:**
- `user_id` passed to form constructor in the route
- Choices populated dynamically based on current user
- Empty choices if no `user_id` (prevents errors)
- `coerce=int` ensures the value is converted to integer

**In the route:**
```python
@orders_bp.route("/new", methods=["GET", "POST"])
@login_required
def order_new():
    user = g.user
    form = OrderCreate(user_id=user.id)  # Pass user_id here
    
    if len(form.customer_id.choices) == 0:
        flash("Please Add customers before orders", "info")
```

This pattern prevents User A from seeing User B's customers in the dropdown.

### The `@login_required` Decorator

Instead of checking `session.get("user_id")` in every route, the decorator handles it:

```python
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper
```

Used like this:
```python
@customers_bp.route("/")
@login_required
def customers():
    # g.user is guaranteed to exist here
```

### Flask-Migrate for Schema Changes

Instead of manually writing SQL migrations, Flask-Migrate generates them:

```bash
# Make changes to models
flask db migrate -m "Add company field to Customer"

# Review the generated migration in migrations/versions/

# Apply it
flask db upgrade
```

This makes schema evolution painless and reversible.

### The Single-Template Password Reset

`forgot_password.html` handles multiple states:

1. **"forgot"** – Email input form
2. **"sent_or_not_found"** – Confirmation message
3. **"error"** – Error state

`reset_password.html` handles:

1. **"reset"** – Password reset form
2. **"success"** – Confirmation message
3. **"error"** – Invalid/expired token

This saves creating separate templates for each state while keeping the logic clear.

### Email Sending Architecture

Password reset emails are handled by `app/mail_utils.py`:

```python
from .extensions import mail
from flask_mail import Message
from flask import render_template

def send_reset_email(to_email, reset_link):
    msg = Message(
        "Business Dashboard",
        recipients=[to_email],
        html=render_template("auth/reset_email.html", reset_link=reset_link),
        body=render_template("auth/reset_email.txt", reset_link=reset_link)
    )
    mail.send(msg)
```

**Key design points:**
- **Both HTML and plain text** – Email clients get appropriate format
- **Template-based** – Email content lives in templates, not Python code
- **Single-purpose function** – Easy to test and maintain
- **Centralized** – All email sending goes through one utility module

**Email templates:**
- `reset_email.html` – Styled HTML version with buttons/formatting
- `reset_email.txt` – Plain text fallback for old email clients

This separation makes it easy to add more email types later (order confirmations, customer notifications, etc.) by adding new functions to `mail_utils.py`.

---

## Production Deployment

### Gunicorn Configuration

The included `gunicorn.conf.py` has production-ready defaults with environment variable overrides:

```python
import os

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.getenv("GUNICORN_WORKERS", 4))
timeout = int(os.getenv("GUNICORN_TIMEOUT", 30))

accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
```

**Starting with Gunicorn:**
```bash
# Use default settings (4 workers, port 8000)
gunicorn run:app

# Or with explicit config file
gunicorn --config gunicorn.conf.py run:app

# Override via environment variables
GUNICORN_WORKERS=8 GUNICORN_BIND=127.0.0.1:5000 gunicorn run:app
```

**Configuration options:**
- `GUNICORN_BIND` – Address and port to bind (default: `0.0.0.0:8000`)
- `GUNICORN_WORKERS` – Number of worker processes (default: 4, adjust based on CPU cores)
- `GUNICORN_TIMEOUT` – Worker timeout in seconds (default: 30)

### Environment Variables for Production

Set these in your production environment (not in `.env` file):
```bash
export FLASK_ENV=production
export SECRET_KEY="generate-a-new-secure-key"
export DATABASE_URL="sqlite:///var/www/business-dashboard/instance/business.db"
export BUSINESS_DASHBOARD_EMAIL="noreply@yourdomain.com"
export BUSINESS_DASHBOARD_EMAIL_PASSWORD="your-production-smtp-password"
export MAIL_SERVER="smtp.your-email-provider.com"
```

**Security checklist:**
- [ ] Generate a new `SECRET_KEY` (don't reuse dev key)
- [ ] Use absolute paths for `DATABASE_URL` in production
- [ ] Ensure database file is writable by Gunicorn user
- [ ] Configure firewall to only allow nginx → Gunicorn traffic
- [ ] Set up HTTPS with valid SSL certificate

### Reverse Proxy Setup (nginx example)

```nginx
upstream business_dashboard {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;  # Force HTTPS
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://business_dashboard;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    location /static {
        alias /var/www/business-dashboard/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Get SSL certificate (Let's Encrypt):**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### systemd Service (recommended)

Create `/etc/systemd/system/business-dashboard.service`:
```ini
[Unit]
Description=Business Dashboard Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/business-dashboard
Environment="PATH=/var/www/business-dashboard/venv/bin"
EnvironmentFile=/var/www/business-dashboard/.env
ExecStart=/var/www/business-dashboard/venv/bin/gunicorn --config gunicorn.conf.py run:app

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable business-dashboard
sudo systemctl start business-dashboard
sudo systemctl status business-dashboard
```

---

## Known Limitations

- ⚠️ **No file uploads** – Orders can't have attachments or invoices
- ⚠️ **No bulk operations** – Can't delete multiple customers at once
- ⚠️ **Email only works with SMTP** – No support for SendGrid/Mailgun APIs
- ⚠️ **SQLite limitations** – Not suitable for 100+ concurrent users
- ⚠️ **No audit trail** – Can't see who edited what and when
- ⚠️ **No export functionality** – Can't export customer/order lists to CSV
- ⚠️ **Basic search** – No filtering or search on customer/order pages
- ⚠️ **No date range queries** – Can't filter orders by date
- ⚠️ **Fixed pagination** – Always 10 items per page (not configurable)
- ⚠️ **No API** – Data only accessible through web interface

---

## Future Improvements

- [ ] Add CSV export for customers and orders
- [ ] Implement search and filtering on list pages
- [ ] Add date range picker for order queries
- [ ] Support file uploads (invoices, receipts, contracts)
- [ ] Build a REST API for programmatic access
- [ ] Add audit logging (who changed what, when)
- [ ] Support multiple currencies
- [ ] Add order item line items (multiple products per order)
- [ ] Implement order status transitions (pending → processing → completed)
- [ ] Add email notifications when order status changes
- [ ] Dashboard charts (revenue over time, top customers)
- [ ] Dark mode toggle
- [ ] Mobile app (React Native or Flutter)
- [ ] Bulk operations (delete multiple, export selected)
- [ ] Advanced permissions (admin vs user roles)

---

## What I Learned

### The Join Query Pattern

Initially I was doing this:
```python
# Bad: Two queries, N+1 problem potential
user_customers = Customer.query.filter_by(user_id=user.id).all()
for customer in user_customers:
    orders = Order.query.filter_by(customer_id=customer.id).all()
```

Learned to use joins instead:
```python
# Good: Single query with join
orders = Order.query.join(Customer).filter(Customer.user_id == user.id).all()
```

Much faster and cleaner.

### Form Validation Is Subtle

WTForms' custom validators took a while to understand. The key insights:

1. Method must be named `validate_<field_name>`
2. Automatically called during `form.validate_on_submit()`
3. Raise `ValidationError` to display error message
4. Can access other form fields via `self`

**Edit forms need extra context:**
```python
class CustomerEdit(BaseForm):
    def __init__(self, customer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer  # Pass current customer to exclude from duplicate check
```

Without this, editing a customer would always fail validation (email conflicts with itself).

### Pagination Boilerplate

SQLAlchemy's pagination is straightforward:
```python
pagination = Customer.query.filter_by(user_id=user.id).paginate(
    page=page, 
    per_page=10, 
    error_out=False
)

customers = pagination.items  # Current page items
```

**Template access:**
```html
{% if pagination.has_prev %}
    <a href="{{ url_for('customers.customers', page=pagination.prev_num) }}">Previous</a>
{% endif %}

{% if pagination.has_next %}
    <a href="{{ url_for('customers.customers', page=pagination.next_num) }}">Next</a>
{% endif %}
```

### The Orphan Delete Problem

Original code allowed deleting customers with orders, which left orphaned order records. Fix:

```python
# Check for existing orders before delete
if Order.query.filter_by(customer_id=id).first():
    flash("Cannot delete customer with existing orders.", "danger")
    return redirect(url_for("customers.customers"))

# Safe to delete
db.session.delete(customer)
db.session.commit()
```

Better than relying on database-level cascade rules.

### Flask-Migrate Saved My Sanity

Early on, I was manually editing the database file every time I changed a model. Flask-Migrate is magic:

```bash
# Change model
class Customer(db.Model):
    company = db.Column(db.String(100))  # Added this field

# Generate migration
flask db migrate -m "Add company field"

# Apply it
flask db upgrade
```

Migrations are version-controlled, reversible, and shareable. Game changer.

### Production Readiness Is About Structure

Initially this was a single-file Flask app with routes, models, and forms all mixed together. Refactoring to blueprints, separate form classes, and the application factory pattern made deployment actually possible.

**What changed:**
- Single `app.py` → Organized blueprints (`auth`, `orders`, `customers`)
- Global `app` instance → Application factory (`create_app()`)
- Forms inline in routes → Dedicated form classes with validation
- Password logic scattered → Centralized in `models/user.py`
- Email code in routes → Utility module (`mail_utils.py`)

**Why it matters:**
- Each blueprint can be tested independently
- Config can be injected (dev vs prod)
- Forms are reusable and self-documenting
- Gunicorn can import and run multiple workers
- New developers can navigate the codebase

The actual business logic didn't change much. The structure changed everything.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
**Problem:** Running Python from wrong directory  
**Solution:**
```bash
cd /path/to/business-dashboard
python run.py
```

### "RuntimeError: Missing required environment variables"
**Problem:** Environment variables not set  
**Solution:** Check your `.env` file has all required vars:
```bash
SECRET_KEY=...
DATABASE_URL=sqlite:///instance/business.db
MAIL_SERVER=...
BUSINESS_DASHBOARD_EMAIL=...
BUSINESS_DASHBOARD_EMAIL_PASSWORD=...
```

If you see "Missing: MAIL_USERNAME" on startup, it means `BUSINESS_DASHBOARD_EMAIL` is not set (the config internally uses `MAIL_USERNAME` as the attribute name).

### "No such table: users"
**Problem:** Database not initialized  
**Solution:**
```bash
flask db upgrade
```

### "SMTPAuthenticationError: Username and Password not accepted"
**Problem:** Using regular Gmail password instead of app password  
**Solution:**
1. Enable 2FA on Google account
2. Generate app-specific password
3. Use that password in `MAIL_PASSWORD`

### "Cannot delete customer with existing orders"
**Problem:** Trying to delete a customer who has orders  
**Solution:** Delete the customer's orders first, then delete the customer

### "Email is connected to another customer"
**Problem:** Trying to use an email that's already registered  
**Solution:** Use a different email address (emails must be unique)

### "Order number already registered"
**Problem:** Trying to create an order with a duplicate order number  
**Solution:** Use a unique order number (within your account)

### Pagination not working
**Problem:** Page numbers in URL but still showing first page  
**Solution:** Check route accepts `page` parameter:
```python
page = request.args.get("page", 1, type=int)
```

### Password reset email not sending
**Problem:** Mail configuration incorrect  
**Solution:**
1. Verify SMTP settings:
```python
# Test connection
from flask_mail import Mail, Message
mail = Mail(app)
msg = Message("Test", recipients=["test@example.com"])
mail.send(msg)
```
2. Check spam folder
3. Verify `BUSINESS_DASHBOARD_EMAIL` is set correctly (used as sender address)

### Users seeing each other's data
**Problem:** Missing `user_id` filter in queries  
**Solution:** Always include user filter:
```python
# Wrong
customers = Customer.query.all()

# Correct
customers = Customer.query.filter_by(user_id=user.id).all()
```

---

## License

MIT License – use it, modify it, deploy it, sell it. Do whatever you want with it.