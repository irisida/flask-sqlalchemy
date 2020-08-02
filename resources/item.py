from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="The price field is required",
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="The store_id field is required",
    )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    # @jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return (
                {"message": "Item '{}' already exists".format(name)},
                400,
            )

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        print("DEBUG: ", item.json())
        item.save_to_db()
        return item.json(), 201

    # @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"Message": "Item deleted"}

    # @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        item.save_to_db()
        return item.json()
