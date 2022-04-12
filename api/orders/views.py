from flask_restx import Namespace,Resource


order_ns = Namespace('Order',description='A namespace for order')

@order_ns.route('/')
class OrderResource(Resource):
    def get(self):
        return {'msg':'Hello get'}

    def post(self):
        return {'msg':'Hello post'}

@order_ns.route('/<int:id>')
class OrderResource(Resource):
    def get(self,id):
        return {'msg':'Hello'}

    def put(self,id):
        return {'msg':'Hello put'}
    
    def delete(self,id):
        return {'msg':'Hello delete'}