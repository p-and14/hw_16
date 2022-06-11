import json
from datetime import datetime


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


def user_instance_to_dict(instance):
    """
    Serialize implementation
    """
    return {
            "id": instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "age": instance.age,
            "email": instance.email,
            "role": instance.role,
            "phone": instance.phone,
        }


def order_instance_to_dict(instance):
    """
    Serialize implementation
    """
    return {
            "id": instance.id,
            "name": instance.name,
            "description": instance.description,
            "start_date": instance.start_date,
            "end_date": instance.end_date,
            "address": instance.address,
            "price": instance.price,
            "customer_id": instance.customer_id,
            "executor_id": instance.executor_id,
        }


def offer_instance_to_dict(instance):
    """
    Serialize implementation
    """
    return {
            "id": instance.id,
            "order_id": instance.order_id,
            "executor_id": instance.executor_id,
        }
