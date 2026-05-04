import csv
import json
from io import StringIO

from email_validator import EmailNotValidError, validate_email

from app.models import Customer, Order

VALID_STATUSES = {"pending", "processing", "completed", "cancelled"}


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
        if not isinstance(payload, list):
            raise ValueError("JSON file must contain a list of records.")
        return [_normalize_row(row) for row in payload if isinstance(row, dict)]

    raise ValueError("Upload a CSV or JSON file.")


def validate_customer_import(rows, user_id):
    errors = []
    valid_rows = []
    seen_emails = set()
    existing_emails = {
        customer.email.lower()
        for customer in Customer.query.with_entities(Customer.email).all()
    }

    for index, row in enumerate(rows, start=2):
        name = row.get("name", "")
        email = row.get("email", "").lower()
        phone = row.get("phone", "")
        company = row.get("company", "")
        row_errors = []

        if not name:
            row_errors.append("name is required")
        if not email:
            row_errors.append("email is required")
        else:
            try:
                email = validate_email(email, check_deliverability=False).normalized.lower()
            except EmailNotValidError:
                row_errors.append("email is invalid")

        if email in seen_emails:
            row_errors.append("email is duplicated in this file")
        if email in existing_emails:
            row_errors.append("email already exists")

        if row_errors:
            errors.append({"row": index, "message": ", ".join(row_errors)})
            continue

        seen_emails.add(email)
        valid_rows.append(
            Customer(
                user_id=user_id,
                name=name,
                email=email,
                phone=phone,
                company=company,
            )
        )

    return valid_rows, errors


def validate_order_import(rows, user_id):
    errors = []
    valid_rows = []
    seen_order_numbers = set()
    pending_customers = {}
    customer_by_email = {
        customer.email.lower(): customer
        for customer in Customer.query.filter_by(user_id=user_id).all()
    }
    all_customer_emails = {
        customer.email.lower()
        for customer in Customer.query.with_entities(Customer.email).all()
    }
    existing_order_numbers = {
        order.order_number.lower()
        for order in Order.query.with_entities(Order.order_number).all()
    }

    for index, row in enumerate(rows, start=2):
        order_number = row.get("order_number", "")
        customer_email = row.get("customer_email", "").lower()
        customer_name = row.get("customer_name", "")
        customer_phone = row.get("customer_phone", "")
        customer_company = row.get("customer_company", "")
        product = row.get("product", "")
        status = (row.get("status") or "pending").lower()
        row_errors = []

        quantity = _parse_int(row.get("quantity"))
        price = _parse_float(row.get("price"))

        if not order_number:
            row_errors.append("order_number is required")
        if not customer_email:
            row_errors.append("customer_email is required")
        if not product:
            row_errors.append("product is required")
        if quantity is None or quantity < 1:
            row_errors.append("quantity must be 1 or greater")
        if price is None or price < 0:
            row_errors.append("price must be 0 or greater")
        if status not in VALID_STATUSES:
            row_errors.append("status is invalid")

        order_key = order_number.lower()
        if order_key in seen_order_numbers:
            row_errors.append("order_number is duplicated in this file")
        if order_key in existing_order_numbers:
            row_errors.append("order_number already exists")

        customer = customer_by_email.get(customer_email)
        if customer_email and customer is None:
            customer = pending_customers.get(customer_email)

        if customer_email and customer is None:
            if customer_email in all_customer_emails:
                row_errors.append("customer_email already belongs to another customer")
            elif not customer_name:
                row_errors.append("customer_name is required when customer_email is new")
            else:
                try:
                    normalized_email = validate_email(
                        customer_email, check_deliverability=False
                    ).normalized.lower()
                except EmailNotValidError:
                    row_errors.append("customer_email is invalid")
                else:
                    customer = Customer(
                        user_id=user_id,
                        name=customer_name,
                        email=normalized_email,
                        phone=customer_phone,
                        company=customer_company,
                    )
                    pending_customers[normalized_email] = customer
                    customer_by_email[normalized_email] = customer

        if row_errors:
            errors.append({"row": index, "message": ", ".join(row_errors)})
            continue

        seen_order_numbers.add(order_key)
        order = Order(
            order_number=order_number,
            product=product,
            quantity=quantity,
            price=price,
            status=status,
        )
        order.customer = customer
        valid_rows.append(order)

    return [*pending_customers.values(), *valid_rows], errors


def _normalize_row(row):
    return {
        str(key).strip().lower(): "" if value is None else str(value).strip()
        for key, value in row.items()
    }


def _parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
