from flask import jsonify, request,make_response
from flask_restx import Namespace,Resource,fields
from sqlalchemy import true
from werkzeug.security import generate_password_hash,check_password_hash
from api.models.users import User
from werkzeug.exceptions import Conflict,BadRequest
from http import HTTPStatus
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity

auth_ns = Namespace('Auth',description='A namespace for authentication')


signup_model=auth_ns.model(
    'SignUp',{
        'username':fields.String(required=True,description="Enter username"),
        'email':fields.String(required=True,description="Enter email"),
        'password':fields.String(required=True,description="Enter password"),
    }
)
user_model = auth_ns.model(
    'User',{
        'username':fields.String(required=True,description="username"),
        'email':fields.String(required=True,description="email"),
        'is_active':fields.Boolean(description="This shows that User is active"),
        'is_staff':fields.Boolean(description="This shows that User is staff"),
    }
)


login_model=auth_ns.model(
    'Login',{
        'email':fields.String(required=True,description="Enter email"),
        'password':fields.String(required=True,description="Enter password")
    }
)


@auth_ns.route('/signup')
class SignupResource(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.marshal_with(user_model)
    def post(self):
        """
        Create a new User
        """
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        try:
            new_user = User(
            email=email,
            username=username,
            password=generate_password_hash(password)
            )
            new_user.save()
            return new_user,HTTPStatus.CREATED
        except Exception as e:
            raise Conflict(f"User with email {email} exists")

@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """
        Generate JWT Token
        """
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return make_response(jsonify({
                'acess_token':access_token,
                'refresh_token':refresh_token
            }),HTTPStatus.OK)
        return jsonify({'error':'Invalid Credentials'})


@auth_ns.route('/refresh')
class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)
        return make_response(jsonify({
                'acess_token':access_token,
            }),HTTPStatus.OK)