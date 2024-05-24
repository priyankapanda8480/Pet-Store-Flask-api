from flask import Blueprint, request, jsonify
from models import db, Category, Dog

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/add_category', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')
    category_type = data.get('type')

    if not name or not category_type:
        return jsonify({'error': 'Name and type are required'}), 400

    new_category = Category(name=name, type=category_type)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully'}), 201

@admin_bp.route('/category/number', methods=['POST'])
def add_dogs():
    try:
        data = request.get_json()
        category_id = data.get('category_id')
        number = data.get('number')

        if not category_id or not number:
            return jsonify({'error': 'Category ID and number are required'}), 400

        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        # Check if the category already has 20 dogs
        current_dogs_count = Dog.query.filter_by(category_id=category_id).count()
        if current_dogs_count + number > 20:
            return jsonify({'error': 'Cannot exceed maximum of 20 dogs per category'}), 400

        # Add dogs to the category
        for _ in range(number):
            dog = Dog(name=f'Dog {_+1}', category_id=category_id)
            db.session.add(dog)

        db.session.commit()
        return jsonify({'message': f'{number} dogs added to category {category.name}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/show_category', methods=['GET'])
def show_category():
    categories = Category.query.all()
    result = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify(result), 200

@admin_bp.route('/list_dog', methods=['GET'])
def list_dogs():
    categories = Category.query.all()
    result = []
    for category in categories:
        dogs = Dog.query.filter_by(category_id=category.id).all()
        result.append({
            'category': category.name,
            'dogs': [{'id': dog.id, 'name': dog.name, 'is_sold': dog.is_sold} for dog in dogs]
        })
    return jsonify(result), 200

@admin_bp.route('/dog/<int:dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    try:
        dog = Dog.query.get(dog_id)
        if not dog:
            return jsonify({'error': 'Dog not found'}), 404

        db.session.delete(dog)
        db.session.commit()

        return jsonify({'message': f'Dog {dog_id} deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
