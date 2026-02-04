from app.extensions import db


class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product = db.Column(db.String(200), nullable=False, )
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(50), default='pending')
    created = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    @property
    def total_amount(self):
        return self.quantity * self.price

    def __repr__(self):
        return f"<Order: {self.order_number}>"
