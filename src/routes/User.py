from flask import Blueprint, jsonify, request, redirect
from models.user import User
from utils.extensions import db
from models.userSchema import user_register_schema, user_login_schema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
import uuid

user_route=Blueprint('user_blueprint', __name__)

@user_route.route('/register', methods=['POST'])
def register():
    data = user_register_schema.load(request.json)
    id = str(uuid.uuid4())
    username = data['username']
    email = data['email']
    password = data['password']
    print(data)
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "El usuario ya existe"}), 400
    
    new_user = User(id, username, email, password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario registrado exitosamente"}), 201

@user_route.route('/login', methods=['POST'])
def login():
    try:
        data = user_login_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"msg": "Error de validación", "errors": err.messages}), 400
    
    username_or_email = data['username']
    password = data['password']

    if '@' in username_or_email:
        user = User.query.filter_by(email=username_or_email).first()
    else: 
        user = User.query.filter_by(username=username_or_email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

@user_route.route('/profile', methods=['GET'])
@jwt_required()
def show_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    return jsonify({
            "username": user.username,
            "id": user.id
        }), 200