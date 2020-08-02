from werkzeug.security import safe_str_cmp
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)


class Login(Resource):
    def post(self):
        print("DEBUG", request)
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        username = request.json.get("username", None)
        password = request.json.get("password", None)

        print("DEBUG: ", username, " :", password)

        if not username:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        if authenticate(username, password):
            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=username)
            print("DEBUG - : ", username, password, access_token)
            return make_response(jsonify(access_token=access_token), 200)
