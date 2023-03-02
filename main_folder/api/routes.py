from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car_Collection, inventory_schema, inventories_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/inventories', methods = ['POST'])
@token_required
def create_inventory(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    inventory = Car_Collection(make, model, year, user_token=user_token)

    db.session.add(inventory)
    db.session.commit()

    response = inventory_schema.dump(inventory)
    return jsonify(response)

@api.route('/inventories', methods = ['GET'])
@token_required
def get_inventory(current_user_token):
    a_user = current_user_token.token
    inventories = Car_Collection.query.filter_by(user_token = a_user).all()
    response = inventories_schema.dump(inventories)
    return jsonify(response)