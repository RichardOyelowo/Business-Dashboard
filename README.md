<div align="center">

# <img src="images/logo.svg" alt="Business Dashboard Logo" style="vertical-align: middle;">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg)](https://flask.palletsprojects.com/)
![Status](https://img.shields.io/badge/status-MVP-success.svg)

A Flask business dashboard for customers, orders, imports, and revenue insight.

</div>

---

## Description

Business Dashboard is a small business management app I built because I wanted something more useful than a spreadsheet but not as heavy as a full CRM.

The app gives users a place to manage customers, track orders, import existing records, and see business activity from a private dashboard.

The current version has:

- A public homepage for visitors
- Auth pages for signup, login, logout, and password reset
- A logged-in dashboard with charts and metrics
- Customer and order management
- CSV and JSON import for bulk data
- User-specific data isolation

Each user only sees their own customers and orders.

---

![Business Dashboard Homepage](images/image.webp)

---

## Project Goal

The goal is simple:

> Sign up, add or import customers, add or import orders, then see useful business insight.

I wanted the MVP to answer these questions quickly:

1. Who are my customers?
2. What orders do I have?
3. How much revenue is in the system?
4. Which orders are pending?
5. Which customers are bringing in the most revenue?

That is why the app keeps orders connected to customers instead of treating them as separate records.

---

## Features

### Public Site

- Public homepage at `/`
- Product explanation
- Login and signup calls to action
- Dashboard preview section
- Import workflow explanation

### Authentication

- Signup
- Login
- Logout
- Password reset email
- Session based user loading
- Protected dashboard and CRUD routes

### Customers

- Create customer
- View customers
- Edit customer
- Delete customer when they have no orders
- Store name, email, phone, company, and created date

### Orders

- Create order
- View orders
- Edit order
- Delete order
- Track order number, customer, product, quantity, price, status, and date
- Calculate order total from quantity and price

### Dashboard

- Total revenue
- Average order value
- Total customers
- Total orders
- Pending orders
- Completed orders
- Revenue over time chart
- Orders by status chart
- Customer growth chart
- Recent orders
- Top customers by revenue

### Imports

- Customer CSV import
- Customer JSON import
- Order CSV import
- Order JSON import
- Order imports match customers by email
- Order imports can create missing customers when customer details are included
- Imports are all-or-nothing so bad rows do not create partial data

---

## Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Backend | Python, Flask | Web app framework |
| Database | SQLAlchemy, SQLite | ORM and persistence |
| Migrations | Flask-Migrate, Alembic | Schema changes |
| Forms | Flask-WTF, WTForms | Forms, validation, CSRF |
| Auth | Werkzeug, itsdangerous | Password hashing and reset tokens |
| Email | Flask-Mail | Password reset emails |
| Frontend | Jinja2, Bootstrap, CSS | Server-rendered UI |
| Charts | Chart.js | Dashboard graphs |

I kept the stack simple on purpose. This app does not need a separate frontend server or a build pipeline. Flask, Jinja, Bootstrap, and Chart.js are enough for the MVP.

---

## Quick Start

Clone the repo:

```bash
git clone <repository-url>
cd Business_Dashboard
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
cat > .env << EOF
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL=sqlite:///dev.db
FLASK_ENV=development
MAIL_SERVER=smtp.gmail.com
BUSINESS_DASHBOARD_EMAIL=your-email@gmail.com
BUSINESS_DASHBOARD_EMAIL_PASSWORD=your-app-password
EOF
```

Run migrations:

```bash
flask db upgrade
```

Start the app:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `SECRET_KEY` | Yes | Flask session and reset token signing key |
| `DATABASE_URL` | Yes in production | Database connection string |
| `FLASK_ENV` | No | `development` or `production` |
| `MAIL_SERVER` | Yes for reset email | SMTP server |
| `BUSINESS_DASHBOARD_EMAIL` | Yes for reset email | Sender email |
| `BUSINESS_DASHBOARD_EMAIL_PASSWORD` | Yes for reset email | SMTP password or app password |

Example:

```bash
SECRET_KEY=change-this-secret
DATABASE_URL=sqlite:///dev.db
FLASK_ENV=development
MAIL_SERVER=smtp.gmail.com
BUSINESS_DASHBOARD_EMAIL=your-email@gmail.com
BUSINESS_DASHBOARD_EMAIL_PASSWORD=your-app-password
```

For Gmail, use an app password.

---

## Project Structure

```text
Business_Dashboard/
  app/
    auth/        login, signup, password reset, decorators
    forms/       WTForms classes
    models/      User, Customer, Order
    routes/      dashboard, customers, orders, imports
    services/    import parsing and validation
    static/      CSS, logos, favicon files
    templates/   Jinja pages
  migrations/
  images/
  tests/
  run.py
  requirements.txt
```

---

## Main Routes

### Public Routes

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/` | Public homepage |
| `GET, POST` | `/signup` | Create account |
| `GET, POST` | `/login` | Login |
| `GET, POST` | `/forgot_password` | Request password reset |
| `GET, POST` | `/reset_password/<token>` | Set new password |

### Protected Routes

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/dashboard` | Main analytics dashboard |
| `POST` | `/logout` | Logout |
| `GET` | `/customers/` | Customer list |
| `GET, POST` | `/customers/new` | Add customer |
| `GET, POST` | `/customers/<id>/edit` | Edit customer |
| `POST` | `/customers/<id>/delete` | Delete customer |
| `GET` | `/orders/` | Order list |
| `GET, POST` | `/orders/new` | Add order |
| `GET, POST` | `/orders/<id>/edit` | Edit order |
| `POST` | `/orders/<id>/delete` | Delete order |
| `GET` | `/imports/` | Import page |
| `POST` | `/imports/customers` | Import customers |
| `POST` | `/imports/orders` | Import orders |

---

## Dashboard

The dashboard lives at `/dashboard`.

It is protected by login and only shows data for the current user.

The backend prepares summary values and chart data before rendering the page.

```python
orders = (
    Order.query.join(Customer)
    .filter(Customer.user_id == user.id)
    .order_by(Order.created.asc())
    .all()
)
```

The dashboard currently shows:

```text
Total Revenue
Average Order
Customers
Total Orders
Pending Orders
Completed Orders
Revenue Over Time
Order Status
Customer Growth
Recent Orders
Top Customers
```

Chart data is passed to the page as JSON:

```python
chart_data = {
    "revenue": {
        "labels": list(revenue_by_day.keys()),
        "values": [round(value, 2) for value in revenue_by_day.values()],
    },
    "statuses": {
        "labels": [status.title() for status in status_counts.keys()],
        "values": list(status_counts.values()),
    },
    "customers": {
        "labels": list(customer_growth.keys()),
        "values": list(customer_growth.values()),
    },
}
```

In the template:

```html
<script>
    const chartData = {{ chart_data|tojson }};
</script>
```

---

## Customers and Orders

Customers are the base records.

Orders belong to customers, and customers belong to users.

This relationship is what makes the dashboard useful. It allows the app to calculate top customers, customer revenue, recent orders, and order status breakdowns.

### Customer Fields

| Field | Required | Notes |
| --- | --- | --- |
| `name` | Yes | Customer name |
| `email` | Yes | Used for import matching |
| `phone` | No | Optional contact info |
| `company` | No | Optional company name |
| `created_at` | Automatic | Database timestamp |

### Order Fields

| Field | Required | Notes |
| --- | --- | --- |
| `order_number` | Yes | Human readable order ID |
| `customer_id` | Yes | Links order to customer |
| `product` | Yes | Product or service |
| `quantity` | Yes | Must be at least 1 |
| `price` | Yes | Must be 0 or greater |
| `status` | Yes | pending, processing, completed, cancelled |
| `created` | Automatic | Database timestamp |

Order total:

```python
@property
def total_amount(self):
    return self.quantity * self.price
```

Customer delete is blocked when the customer has orders:

```python
if customer.orders.first():
    flash("Cannot delete customer with existing orders.", "danger")
    return redirect(url_for("customers.customers"))
```

---

## Bulk Import

Bulk import is part of the MVP because a dashboard needs data before it becomes useful.

Import files can be CSV or JSON.

### Customer CSV

```csv
name,email,phone,company
Jane Smith,jane@example.com,555-1111,Smith Studio
Mark Lee,mark@example.com,555-2222,Lee Consulting
```

### Customer JSON

```json
{
  "customers": [
    {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "555-1111",
      "company": "Smith Studio"
    }
  ]
}
```

### Order CSV

```csv
order_number,customer_email,customer_name,customer_phone,customer_company,product,quantity,price,status
ORD-1001,jane@example.com,Jane Smith,555-1111,Smith Studio,Website Design,1,1200,completed
ORD-1002,mark@example.com,Mark Lee,555-2222,Lee Consulting,Monthly Support,3,250,pending
```

### Order JSON

```json
{
  "orders": [
    {
      "order_number": "ORD-1001",
      "customer_email": "jane@example.com",
      "customer_name": "Jane Smith",
      "product": "Website Design",
      "quantity": 1,
      "price": 1200,
      "status": "completed"
    }
  ]
}
```

### How Order Import Handles Customers

Orders stay connected to customers.

The importer uses `customer_email` as the matching key.

1. If the email matches one of the user's customers, the order attaches to that customer.
2. If the email is new and `customer_name` exists, the importer creates the customer and attaches the order.
3. If the email is new and `customer_name` is missing, the row fails.
4. If any row fails, nothing is imported.

Validation catches missing fields, invalid emails, duplicate emails, duplicate order numbers, invalid statuses, bad quantity, and bad price.

---

## Database Design

Main models:

| Model | Purpose | Relationship |
| --- | --- | --- |
| `User` | Account owner | Has many customers |
| `Customer` | Customer profile | Belongs to a user and has many orders |
| `Order` | Revenue or work item | Belongs to a customer |

Relationship summary:

```text
User has many Customers
Customer has many Orders
Order belongs to one Customer
Customer belongs to one User
```

Order model:

```python
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    product = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(50), default="pending")
```

Orders do not store `user_id` directly. Ownership comes through the customer relationship.

---

## Security and Data Isolation

Every logged-in user has a private workspace.

Customer queries filter by `user_id`:

```python
pagination = Customer.query.filter_by(user_id=user.id).order_by(
    Customer.created_at.desc()
).paginate(page=page, per_page=10, error_out=False)
```

Order queries join through customers:

```python
pagination = (
    Order.query.join(Customer)
    .filter(Customer.user_id == user.id)
    .order_by(Order.created.desc())
    .paginate(page=page, per_page=10, error_out=False)
)
```

The main rule is:

```text
Do not query customer or order records without checking ownership.
```

Auth uses sessions. The current user is loaded before each request:

```python
@app.before_request
def activate_current_user():
    user_id = session.get("user_id")
    g.user = db.session.get(User, user_id) if user_id else None
```

Passwords are hashed with Werkzeug. Password reset tokens use `itsdangerous` and expire after one hour.

---

## Architecture

The project uses a Flask app factory, blueprints, SQLAlchemy models, WTForms forms, Jinja templates, and a small service layer.

Blueprints:

```text
auth       signup, login, logout, password reset
index      public homepage and dashboard
customers  customer CRUD
orders     order CRUD
imports    CSV and JSON uploads
```

Import logic is kept out of the route file:

```text
app/services/imports.py
```

That keeps the import routes focused on request handling and the service focused on parsing and validation.

The UI uses one shared layout:

```text
app/templates/layout.html
```

---

## Code Samples

Homepage route:

```python
@index_bp.route("/")
def index():
    return render_template("home.html")
```

Import parser:

```python
def parse_uploaded_rows(uploaded_file, record_key):
    filename = (uploaded_file.filename or "").lower()
    raw_content = uploaded_file.read().decode("utf-8-sig")

    if filename.endswith(".csv"):
        reader = csv.DictReader(StringIO(raw_content))
        return [_normalize_row(row) for row in reader]

    if filename.endswith(".json"):
        payload = json.loads(raw_content)
        if isinstance(payload, dict):
            payload = payload.get(record_key, [])
        return [_normalize_row(row) for row in payload if isinstance(row, dict)]

    raise ValueError("Upload a CSV or JSON file.")
```

---

## Checks

Checks used before pushing:

```bash
venv/bin/python -m compileall -q app
git diff --check
```

Route smoke checks were run for the public pages, protected pages, customer pages, order pages, and import pages.

Import smoke checks were run for customer CSV import, order CSV import with an existing customer, and order CSV import that creates a missing customer.

`pytest` is not installed in the local virtual environment yet. A proper test suite should be added next.

---

## Deployment Notes

The repo includes a Gunicorn config:

```python
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.getenv("GUNICORN_WORKERS", 4))
timeout = int(os.getenv("GUNICORN_TIMEOUT", 30))
```

Run with Gunicorn:

```bash
gunicorn --config gunicorn.conf.py run:app
```

Production should include a strong `SECRET_KEY`, a production database URL, working SMTP credentials, HTTPS, a reverse proxy, and `flask db upgrade` during deploy.

---

## Troubleshooting

### App prints missing mail values

Set `BUSINESS_DASHBOARD_EMAIL`, `BUSINESS_DASHBOARD_EMAIL_PASSWORD`, and `MAIL_SERVER`.

The app can render pages without email credentials, but password reset emails will not send.

### Database tables do not exist

Run:

```bash
flask db upgrade
```

### Customer cannot be deleted

The customer probably has orders. Delete the customer's orders first, then delete the customer.

### Order import fails

Check `order_number`, `customer_email`, `product`, `quantity`, `price`, and `status`. If the customer email is new, also include `customer_name`.

---

## What I Learned

Order ownership works through customers, so safe order queries need a join:

```python
Order.query.join(Customer).filter(Customer.user_id == user.id)
```

Bulk import should not break the data model. Matching orders by customer email keeps imports practical while preserving customer revenue and order history.

A dashboard also needs fast data entry. Charts are not useful if users have to type every record one by one.

The homepage matters too. `/` now explains the product, while `/dashboard` is the private workspace.

---

## Next Improvements

- Add a real pytest suite
- Add search and filters
- Add date range filters on the dashboard
- Add CSV export
- Add import preview before saving
- Add per-user uniqueness at the database level
- Add account settings
- Add customer detail pages
- Add monthly revenue comparison

---

## License

MIT License.

Use it, modify it, deploy it, and build on top of it.

<div align="center">

Built for the love of development by Richard Oyelowo

</div>
