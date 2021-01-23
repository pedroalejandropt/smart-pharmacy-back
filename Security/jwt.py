from flask import Flask, Blueprint, jsonify, request, abort
from datetime import datetime, timedelta 
from Models.user import User
from config import app, db
from functools import wraps
import jwt

# decorator for verifying the JWT 
def token_required(f): 
    @wraps(f) 
    def decorated(*args, **kwargs): 
        token = None
        # jwt is passed in the request header 
        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token'] 
        # return 401 if token is not passed 
        if not token: 
            return jsonify({'message' : 'Token is missing !!'}), 401
   
        try: 
            # decoding the payload to fetch the stored details 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(email = data['public_id']).first() 
        except: 
            return jsonify({ 
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes 
        return  f(current_user, *args, **kwargs) 
   
    return decorated 

def generate_token(email):
    return jwt.encode({ 
        'public_id': email, 
        'exp' : datetime.utcnow() + timedelta(minutes = 30) 
    }, app.config['SECRET_KEY']) 