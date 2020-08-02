import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db
from security import Login
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "flaskymcflaskface"
api = Api(app)
jwt = JWTManager(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# signup and authentocation
api.add_resource(UserRegister, "/signup")
api.add_resource(Login, "/auth")

# application functionality
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
