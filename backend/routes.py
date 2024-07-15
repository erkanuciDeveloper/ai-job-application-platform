# backend/routes.py

from flask import request, jsonify
from backend import app, db
from backend.models import User
from flask_jwt_extended import jwt_required, create_access_token

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify(message='Username already exists'), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message='User registered successfully'), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify(message='Invalid username or password'), 401

    access_token = user.generate_access_token()

    return jsonify(access_token=access_token), 200
