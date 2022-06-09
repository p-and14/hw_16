import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


def add_users(User, db):
    with open("users.json", "r") as f:
        users = json.load(f)

    for user in users:
        db.session.add(User(
            id=user.get("id"),
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            age=user.get("age"),
            email=user.get("email"),
            role=user.get("role"),
            phone=user.get("phone"),
        ))


def add_orders(Order, db):
    with open("orders.json", "r") as f:
        orders = json.load(f)

    for order in orders:
        db.session.add(Order(
            id=order.get("id"),
            name=order.get("name"),
            description=order.get("description"),
            start_date=datetime.strptime(order.get("start_date"), "%m/%d/%Y"),
            end_date=datetime.strptime(order.get("end_date"), "%m/%d/%Y"),
            address=order.get("address"),
            price=order.get("price"),
            customer_id=order.get("customer_id"),
            executor_id=order.get("executor_id"),
        ))


def add_offers(Offer, db):
    with open("offers.json", "r") as f:
        offers = json.load(f)

    for offer in offers:
        db.session.add(Offer(
            id=offer.get("id"),
            order_id=offer.get("order_id"),
            executor_id=offer.get("executor_id"),
        ))


def db_connect(app):
    db = SQLAlchemy(app)

    class User(db.Model):
        __tablename__ = "users"

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(20), nullable=False)
        last_name = db.Column(db.String(20), nullable=False)
        age = db.Column(db.Integer)
        email = db.Column(db.String(40))
        role = db.Column(db.String(40))
        phone = db.Column(db.String(20))

    class Offer(db.Model):
        __tablename__ = "offers"

        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
        orders = db.relationship("Order")
        executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        users = db.relationship("User")

    class Order(db.Model):
        __tablename__ = "orders"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(20), nullable=False)
        description = db.Column(db.String(500))
        start_date = db.Column(db.DateTime)
        end_date = db.Column(db.DateTime)
        address = db.Column(db.String(100))
        price = db.Column(db.Integer, nullable=False)
        customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    db.create_all()
    add_users(User, db)
    add_orders(Order, db)
    add_offers(Offer, db)

    db.session.commit()

    return User, Order, Offer
