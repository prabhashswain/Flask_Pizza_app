from flask import Flask
from flask_restx import Api
from api.auth.views import auth_ns
from api.orders.views import order_ns
from api.utils import db
from flask_migrate import Migrate
from api.models.orders import Order
from api.models.users import User
from flask_jwt_extended import JWTManager

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    jwt = JWTManager(app)


    db.init_app(app)
    migrate = Migrate(app,db)
    
    authorizations={
        "Bearer Auth":{
            'type':"apiKey",
            'in':'header',
            'name':"Authorization",
            'description':"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }
    
    api = Api(app,doc='/docs',version='1.0', 
    title="Pizza Delivery API",
        description="A REST API for a Pizza Delievry service",
        authorizations=authorizations,
        security="Bearer Auth"
    )
    api.add_namespace(auth_ns,path='/api/v1/auth')
    api.add_namespace(order_ns,path='/api/v1/order')

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "users":User,
            "orders":Order
        }


    return app