from flask_restx import Namespace,Resource,fields


auth_ns = Namespace('Auth',description='A namespace for authentication')


signup_model=auth_ns.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="Enter username"),
        'email':fields.String(required=True,description="Enter email"),
        'password':fields.String(required=True,description="Enter password"),
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
    def post(self):
        return {'msg':'Hello Signup'}

@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def get(self):
        return {'msg':'Hello Login'}