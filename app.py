from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, ValidationError, validate
from flask_marshmallow import Marshmallow
from password import my_password

# Establishing a connection as well as Marshmallow for serialization and deserialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@localhost/e_commerce_project'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Setting up classes and shemas to modify and review later
# TODO: Double check classes and schemas for consistency with ERD
# TODO: Verify all relationships are placed properly.
# TODO: After a class and schema is made, create a new file and import into the app.py

# Schemas needed for this app are below
class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    date_of_birth = fields.Date(nullable=False)
    address = fields.String(required=True)

    class Meta:
        fields = ("name", "email", "date_of_birth", "address", "id")

class CustomerAccountSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        fields = ("username", "password", "id")

class OrderSchema(ma.Schema):
    order_date = fields.Date(required=True)
    status = fields.String(required=True)
    close_date = fields.String(required=False)
    total = fields.Float(required=True, validate=validate.Range(min=0))

    class Meta:
        fields = ("order_date", "status", "close_date", "total", "id")

class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    par_inventory = fields.Integer(required=True)
    current_invenotory = fields.Integer(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))

    class Meta:
        fields = ("name", "par_inventory", "current_inventory", "price")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

customer_account_schema = CustomerAccountSchema()
customers_account_schema = CustomerAccountSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Classes with table names for this app are below

class Customer(db.Model):
    __tablename__ = "Customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(350), nullable=False)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(350), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('CustomerAccounts.id'))

customer_account = db.Table("Customer_Account",
                            db.Column('customer_id', db.Integer, db.ForeignKey('Customers.id'), primary_key=True),
                            db.Column('account_id', db.Integer, db.ForeignKey('CustomerAccounts.id'), primary_key=True)
                            )

class CustomerAccount(db.Model):
    __tablename__ = "CustomerAccounts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))

customer_orders = db.Table('Customer_Orders',
                           db.Column('account_id', db.Integer, db.ForeignKey('CustomerAccounts.id'), primary_key=True),
                           db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True)
                           )

class Order(db.Model):
    __tablename__ = "Orders"
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(350), nullable=False)
    close_date = db.Column(db.Date)
    order_total = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('CustomerAccounts.id'))
    account_orders = db.relationship('CustomerAccount', backref='account_orders')

product_order = db.Table('Product_Order', 
                         db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'),primary_key=True),
                         db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True)
                         )

class Product(db.Model):
    __tablename__ = "Products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    par_inventory = db.Column(db.Integer, nullable=False)
    current_inventory = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_orders = db.relationship('Order', secondary=product_order, backref=db.backref('orders_of_products'))


# Creates tables in database
with app.app_context():
    db.create_all()


# Runs app in debug mode to allow for real time updating
if __name__ == "__main__":
    app.run(debug=True)