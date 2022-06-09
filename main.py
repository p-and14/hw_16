from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils import user_instance_to_dict, order_instance_to_dict, offer_instance_to_dict
from sql_db import db_connect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)
User, Order, Offer = db_connect(app)


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

    return "Пользователь создан"


@app.route("/users/<int:uid>", methods=["PUT"])
def update_user(uid):
    user = User.query.get(uid)
    data = request.json
    user.first_name = data.get('first_name'),
    user.last_name = data.get('last_name'),
    user.age = data.get('age'),
    user.email = data.get('email'),
    user.role = data.get('role'),
    user.phone = data.get('phone')

    db.session.add(user)
    db.session.commit()

    return "Пользователь обновлён"


if __name__ == "__main__":
    app.run(debug=True, port=1212)
