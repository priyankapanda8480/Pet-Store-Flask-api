from flask import Blueprint, request, jsonify
from models import db, Dog, Category

user_bp = Blueprint('user', __name__)

@user_bp.route('/view_category', methods=['GET'])
def view_category():
    categories = Category.query.all()
    result = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify(result), 200

@user_bp.route('/buy_dog', methods=['POST'])
def buy_dog():
    data = request.get_json()
    dog_ids = data['dog_ids']
    if len(dog_ids) > 2:
        return jsonify({'error': 'Cannot buy more than 2 dogs at a time'}), 400

    dogs = Dog.query.filter(Dog.id.in_(dog_ids)).all()
    for dog in dogs:
        if dog.is_sold:
            return jsonify({'error': f'Dog {dog.id} is already sold'}), 400
        dog.is_sold = True

    db.session.commit()
    return jsonify({'message': 'Dogs purchased successfully'}), 200

