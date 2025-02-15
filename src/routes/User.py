from flask import Blueprint, jsonify, request, redirect, render_template, url_for, session, flash
from models.user import User
from utils.extensions import db
from models.userSchema import user_register_schema, user_login_schema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
import uuid
import json

user_route=Blueprint('user_blueprint', __name__)

@user_route.route("/register", methods=['GET'])
def registerForm():
    return render_template("register.html")

@user_route.route('/register', methods=['POST'])
def register():
    form_username = request.form.get('form_name')
    form_email = request.form.get('form_email')
    form_password = request.form.get('form_password')
    
    data = user_register_schema.load({
        "username": form_username,
        "email": form_email,
        "password": form_password                           
    })
    id = str(uuid.uuid4())
    username = data['username']
    email = data['email']
    password = data['password']
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        flash("El usuario y/o email ya existen", "error")
        return redirect(url_for('user_blueprint.register'))
        # return render_template("register.html", data = {"msg": "El usuario y/o email ya existen"}), 400
    
    new_user = User(id, username, email, password)
    db.session.add(new_user)
    db.session.commit()

    # render_template("login.html", data = {"msg": "Usuario registrado exitosamente"}), 201
    flash('Usuario registrado exitosamente', 'success')
    return redirect(url_for('user_blueprint.login'))

@user_route.route('/login')
def loginForm():
    return render_template("login.html"), 200

@user_route.route('/login', methods=['POST'])
def login():
    try:
        data = user_login_schema.load(request.form)
    except ValidationError as err:
        # return render_template("login.html", data = {"msg": "Error de validación"}), 400
        # return jsonify({"msg": "Error de validación", "errors": err.messages}), 400
        flash('Error de validación', 'error')
        return redirect(url_for('user_blueprint.login'))
    
    username_or_email = data['username']
    password = data['password']

    if '@' in username_or_email:
        user = User.query.filter_by(email=username_or_email).first()
    else: 
        user = User.query.filter_by(username=username_or_email).first()

    if user and user.check_password(password):
        # access_token = create_access_token(identity=user.id)
        # return jsonify(access_token=access_token), 200
        session['user_id'] = user.id
        # return render_template("index.html"), 200
        return redirect(url_for('index'))
    
    # return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401
    flash('Usuario o contraseña incorrectos', 'error')
    return redirect(url_for('user_blueprint.login'))

@user_route.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user_blueprint.login'), code=302)

@user_route.route('/profile', methods=['GET'])
@jwt_required()
def show_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    return jsonify({
            "username": user.username,
            "id": user.id
        }), 200