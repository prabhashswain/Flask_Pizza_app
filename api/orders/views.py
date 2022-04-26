from flask import request
from flask_restx import Namespace,Resource,fields
from api.models.orders import Order
from api.models.users import User
from flask_jwt_extended import jwt_required,get_jwt_identity
from http import HTTPStatus
from api.utils import db


order_ns = Namespace('Order',description='A namespace for order')

order_model = order_ns.model(
    'Order',{
         'id':fields.Integer(required=True,description="ID"),
         'size':fields.String(Required=True,description='Size',
         enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE']
         ),
         'order_status':fields.String(Required=True,description='Order Status',
         enum=['PENDING','IN_TRANSIT','DELIVERED']
         ),
    }
)

@order_ns.route('/')
class OrderResource(Resource):
    @order_ns.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """
        Get all Order
        """
        orders = Order.query.all()
        return orders,HTTPStatus.OK

    @order_ns.expect(order_model)
    @order_ns.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        Create Order
        """
        data = request.get_json()
        user = get_jwt_identity()
        current_user = User.query.filter_by(username=user).first()
        new_order = Order(
            size = data.get('size'),
            order_status = data.get('order_status'),
            flavour = data.get('flavour'),
            quantity = data.get('quantity')
        )
        new_order.user = current_user
        new_order.save()
        return new_order,HTTPStatus.CREATED

@order_ns.route('/<int:id>')
class OrderResource(Resource):
    @order_ns.marshal_with(order_model)
    @jwt_required()
    def get(self,id):
        """
        Get Order By ID
        """
        order = Order.get_order_by_id(id)
        return order,HTTPStatus.OK

    @order_ns.expect(order_model)
    @order_ns.marshal_with(order_model)
    @jwt_required()
    def put(self,id):
        """
        Update Order By ID
        """
        order = Order.get_order_by_id(id)
        data = request.get_json()
        order.quantity=data['quantity']
        order.size=data['size']
        order.flavour=data['flavour']
        db.session.commit()
        return order,HTTPStatus.OK
    
    def delete(self,id):
        """
        Delete Order By ID
        """
        order = Order.get_order_by_id(id)
        order.delete()
        return {'msg':'Order Deleted!!!'},HTTPStatus.NO_CONTENT


