import sqlalchemy.exc
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

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


@app.route("/users")
def users_all():
    users = db.session.query(User).all()
    result = []
    for user in users:
        result.append(user_instance_to_dict(user))

    return jsonify(result)


@app.route("/users/<int:uid>")
def users_one(uid):
    try:
        query = db.session.query(User).get(uid)
        result = user_instance_to_dict(query)
    except AttributeError:
        return f"Нет пользователя с ID: {uid}"

    return jsonify(result)


@app.route("/orders")
def orders_all():
    orders = db.session.query(Order).all()
    result = []
    for order in orders:
        result.append(order_instance_to_dict(order))

    return jsonify(result)


@app.route("/orders/<int:uid>")
def orders_one(uid):
    try:
        query = db.session.query(Order).get(uid)
        result = order_instance_to_dict(query)
    except AttributeError:
        return f"Нет заказа с ID: {uid}"

    return jsonify(result)


@app.route("/offers")
def offers_all():
    offers = db.session.query(Offer).all()
    result = []
    for offer in offers:
        result.append(offer_instance_to_dict(offer))

    return jsonify(result)


@app.route("/offers/<int:uid>")
def offers_one(uid):
    try:
        query = db.session.query(Offer).get(uid)
        result = offer_instance_to_dict(query)
    except AttributeError:
        return f"Нет предложений с ID: {uid}"

    return jsonify(result)


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    try:
        user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            email=data.get('email'),
            role=data.get('role'),
            phone=data.get('phone')
        )
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Неправильные входные данные"

    return "Пользователь создан"


@app.route("/users/<int:uid>", methods=["PUT"])
def update_user(uid):
    try:
        user = User.query.get(uid)
        data = request.json
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.age = data.get('age')
        user.email = data.get('email')
        user.role = data.get('role')
        user.phone = data.get('phone')

        db.session.add(user)
        db.session.commit()

    except sqlalchemy.exc.IntegrityError:
        return "Неправильные входные данные"

    except AttributeError:
        return "Пользователя с таким ID не существует"

    return "Пользователь обновлён"


@app.route("/users/<int:uid>", methods=["DELETE"])
def delete_user(uid):
    try:
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return "Пользователя с таким ID не существует"

    return "Пользователь удалён"


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    try:
        order = Order(
            name=data.get('name'),
            description=data.get('description'),
            start_date=datetime.strptime(data.get("start_date"), "%m/%d/%Y"),
            end_date=datetime.strptime(data.get("end_date"), "%m/%d/%Y"),
            address=data.get('address'),
            price=data.get('price'),
            customer_id=data.get('customer_id'),
            executor_id=data.get('executor_id'),
        )
        db.session.add(order)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Неправильные входные данные"

    return "Заказ создан"


@app.route("/orders/<int:uid>", methods=["PUT"])
def update_order(uid):
    try:
        order = Order.query.get(uid)
        data = request.json
        order.name = data.get('name')
        order.description = data.get('description')
        order.start_date = datetime.strptime(data.get("start_date"), "%m/%d/%Y")
        order.end_date = datetime.strptime(data.get("end_date"), "%m/%d/%Y")
        order.address = data.get('address')
        order.price = data.get('price')
        order.customer_id = data.get('customer_id')
        order.executor_id = data.get('executor_id')

        db.session.add(order)
        db.session.commit()

    except sqlalchemy.exc.IntegrityError:
        return "Неправильные входные данные"

    except AttributeError:
        return "Заказа с таким ID не существует"

    return "Заказ обновлён"


@app.route("/orders/<int:uid>", methods=["DELETE"])
def delete_order(uid):
    try:
        order = Order.query.get(uid)
        db.session.delete(order)
        db.session.commit()

    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return "Заказа с таким ID не существует"

    return "Заказ удалён"


@app.route("/offers", methods=["POST"])
def create_offer():
    data = request.json
    offer = Offer(
        order_id=data.get('order_id'),
        executor_id=data.get('executor_id'),
    )
    db.session.add(offer)
    db.session.commit()

    return "Предложение создано"


@app.route("/offers/<int:uid>", methods=["PUT"])
def update_offer(uid):
    try:
        offer = Offer.query.get(uid)
        data = request.json
        offer.order_id = data.get('order_id')
        offer.executor_id = data.get('executor_id')

        db.session.add(offer)
        db.session.commit()

    except sqlalchemy.exc.IntegrityError:
        return "Неправильные входные данные"

    except AttributeError:
        return "Предложения с таким ID не существует"

    return "Предложение обновлено"


@app.route("/offers/<int:uid>", methods=["DELETE"])
def delete_offer(uid):
    try:
        offer = Offer.query.get(uid)
        db.session.delete(offer)
        db.session.commit()

    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return "Предложения с таким ID не существует"

    return "Предложение удалено"


if __name__ == "__main__":
    app.run(debug=True, port=1212)
