from flask import request
from database.models import User
from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import create_access_token
import datetime

class SignupApi(Resource):
    def post(self):
        ## body = {email, password}
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        try:
            user.save()
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'Couldnt create user because : %s' % e}, 400
   
class LoginApi(Resource):
    def post(self):
        ## body = {email, password}
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Email or password invalid'}, 401

        expires = datetime.timedelta(days=7)
        # Create a new token valid for 7
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200