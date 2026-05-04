from json import JSONDecodeError

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.auth import login_required
from app.extensions import db
from app.models import Order
from app.services.imports import (
    parse_uploaded_rows,
    validate_customer_import,
    validate_order_import,
)

imports_bp = Blueprint("imports", __name__, url_prefix="/imports")


@imports_bp.route("/")
@login_required
def import_home():
    return render_template("imports.html")


@imports_bp.route("/customers", methods=["POST"])
@login_required
def import_customers():
    return _handle_import("customers", validate_customer_import)


@imports_bp.route("/orders", methods=["POST"])
@login_required
def import_orders():
    return _handle_import("orders", validate_order_import)


def _handle_import(record_key, validator):
    uploaded_file = request.files.get("data_file")

    if uploaded_file is None or uploaded_file.filename == "":
        flash("Choose a CSV or JSON file to import.", "danger")
        return redirect(url_for("imports.import_home"))

    try:
        rows = parse_uploaded_rows(uploaded_file, record_key)
    except (UnicodeDecodeError, JSONDecodeError, ValueError) as error:
        return render_template(
            "import_result.html",
            import_type=record_key,
            imported_count=0,
            errors=[{"row": "-", "message": str(error)}],
        )

    records, errors = validator(rows, g.user.id)
    if errors:
        return render_template(
            "import_result.html",
            import_type=record_key,
            imported_count=0,
            errors=errors,
        )

    try:
        db.session.add_all(records)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return render_template(
            "import_result.html",
            import_type=record_key,
            imported_count=0,
            errors=[{"row": "-", "message": "Import conflicts with existing data."}],
        )

    imported_count = sum(1 for record in records if isinstance(record, Order)) if record_key == "orders" else len(records)
    flash(f"Imported {imported_count} {record_key}.", "success")
    return render_template(
        "import_result.html",
        import_type=record_key,
        imported_count=imported_count,
        errors=[],
    )
