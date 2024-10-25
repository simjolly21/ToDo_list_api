# resources/todos.py
from flask import Blueprint, request, jsonify
from app import db
from models import Todo
from flask_jwt_extended import jwt_required, get_jwt_identity

todos_bp = Blueprint('todos', __name__)

@todos_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.get_json()
    title = data['title']
    description = data['description']
    user_id = get_jwt_identity()

    todo = Todo(title=title, description=description, user_id=user_id)
    db.session.add(todo)
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "description": todo.description}), 201

@todos_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    todo = Todo.query.get_or_404(todo_id)

    if todo.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403

    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "description": todo.description}), 200

@todos_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.get_or_404(todo_id)

    if todo.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403

    db.session.delete(todo)
    db.session.commit()
    return '', 204

@todos_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    todos = Todo.query.filter_by(user_id=user_id).paginate(page=page, per_page=limit)
    data = [{"id": todo.id, "title": todo.title, "description": todo.description} for todo in todos.items]
    return jsonify({"data": data, "page": page, "limit": limit, "total": todos.total})
