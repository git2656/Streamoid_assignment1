from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    sku = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))
    mrp = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "brand": self.brand,
            "color": self.color,
            "size": self.size,
            "mrp": self.mrp,
            "price": self.price,
            "quantity": self.quantity
        }
