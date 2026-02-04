from app.extensions import db


class Customer(db.Model):
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<Customer: {self.name} - Company: {self.company}>"

    orders = db.relationship('Order', backref='customer', lazy='dynamic')

