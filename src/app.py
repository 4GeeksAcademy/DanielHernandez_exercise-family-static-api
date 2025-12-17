"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# GET /members → obtener todos los miembros
@app.route('/members', methods=['GET'])
def get_all_members():
    return jsonify(jackson_family.get_all_members()), 200


# GET /members/<int:member_id> → obtener un solo miembro
@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)

    if member is None:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify(member), 200


# POST /members → añadir un miembro
@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json()

    if not body:
        return jsonify({"error": "Invalid body"}), 400

    new_member = {
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }

    member = jackson_family.add_member(new_member)
    return jsonify(member), 200


# DELETE /members/<int:member_id> → eliminar miembro
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    
    if not deleted:
        return jsonify({"error": "Member not found"}), 404

    return jsonify({"done": True}), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
