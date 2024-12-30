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
    account_id = fields.Integer(required=True)
    product_ids = fields.List(fields.Integer(),required=False)

    class Meta:
        fields = ("order_date", "status", "close_date", "account_id", "product_ids", "id")

class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    par_inventory = fields.Integer(required=True)
    current_inventory = fields.Integer(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))

    class Meta:
        fields = ("name", "par_inventory", "current_inventory", "price", "id")

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


class CustomerAccount(db.Model):
    __tablename__ = "CustomerAccounts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))

customer_orders = db.Table('Customer_Orders',
                           db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True),
                           db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True)
                           )

class Order(db.Model):
    __tablename__ = "Orders"
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(350), nullable=False)
    close_date = db.Column(db.Date)
    order_total = db.Column(db.Float(10,2), nullable=False, default=0.0)
    account_id = db.Column(db.Integer, db.ForeignKey('CustomerAccounts.id'))

    products = db.relationship('Product', secondary=customer_orders, backref=db.backref('orders', lazy=True))

    def calculate_total(self):
        self.order_total = sum(product.price for product in self.products)

class Product(db.Model):
    __tablename__ = "Products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    par_inventory = db.Column(db.Integer, nullable=False)
    current_inventory = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_orders = db.relationship('Order', secondary=customer_orders, backref=db.backref('orders_of_products'))


# Creates tables in database
with app.app_context():
    db.create_all()

# Routes Separation ----------Preliminary Customer Routes-----------------------------------------

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers)

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        # Validate and desiarlize input
        customer_data = customer_schema.load(request.json)
    
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_customer = Customer(
                            name = customer_data['name'],
                            email = customer_data['email'],
                            date_of_birth = customer_data['date_of_birth'],
                            address = customer_data['address']
                            )
    
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': "New customer added successfully"}), 201


@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        customer_data = customer_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.date_of_birth = customer_data['date_of_birth']
    customer.address = customer_data['address']
    db.session.commit()
    return jsonify({'message': 'Customer details updated successfully'}), 200


@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)#Makes sure customer exists
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer removed successfully.'}), 200

# Routes Separation--------------------------Preliminary Customer Account Routes--------------------------------

@app.route('/customer_accounts', methods=['GET'])
def get_accounts():
    accounts = CustomerAccount.query.all()
    return customers_account_schema.jsonify(accounts)

@app.route('/customer_accounts', methods=['POST'])
def add_customer_account():
    try:
        customer_account_data = customer_account_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_customer_account = CustomerAccount(
                                            username = customer_account_data['username'],
                                            password = customer_account_data['password']
                                            )
    
    db.session.add(new_customer_account)
    db.session.commit()
    return jsonify({"message": "Customer account added successfully."}), 201

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    customer_account = CustomerAccount.query.get_or_404(id)
    try:
        customer_account_data = customer_account_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer_account.username = customer_account_data['username']
    customer_account.password = customer_account_data['password']
    db.session.commit()
    return jsonify({"message": "Customer account updated successfully."}), 200

@app.route('/customer_accounts', methods=['DELETE'])
def delete_customer_account(id):
    customer_account = CustomerAccount.query.get_or_404(id)
    db.session.delete(customer_account)
    db.session.commit()
    return jsonify({"message": "Customer account deleted successfully."}), 200


# Routes Separation---------------------Order Routes---------------------------------------------

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return orders_schema.jsonify(orders)

# TODO: Does the below need to have the foreign key associations with it?
@app.route('/orders', methods=['POST'])
def add_order():
    try:
        order_data = order_schema.load(request.json)
        product_ids = order_data.get('product_ids', [])
        products = Product.query.filter(Product.id.in_(product_ids)).all()

        if not products:
            return jsonify({"error": "No valid products found for the order."}), 400
    
        new_order = Order(
                            order_date = order_data['order_date'],
                            status = order_data['status'],
                            close_date = order_data['close_date'],
                            order_total = order_data['order_total'],
                            account_id = order_data['account_id']
                        )
        
        new_order.products = products
        new_order.calculate_total()

        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order added successfully."}), 201

    except ValidationError as err:
        return jsonify(err.messages), 400

# TODO: Does the below need to have the foreign key associations with it?
@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    try:
        order_data = order_schema.load(request.json)
        product_ids = order_data.get('product_ids',[])
        if product_ids:
            products = Product.query.filter(Product.id.in_(product_ids)).all()
            if not products:
                return jsonify({"error": "No valid products found for the update."}), 400
            order.products = products

        order.order_date = order_data.get('order_date', order.order_date)
        order.status = order_data.get('status', order.status)
        order.close_date = order_data.get('close_date', order.close_date)
        order.calculate_total()

        db.session.commit()
        return jsonify({'message': 'Order updated successfully.'}), 200
    
    except ValidationError as err:
        return jsonify(err.messages), 400


@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)


    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully.'}), 200

# Routes Separation ---------Product Routes-----------------------------------

@app.route('/products', methods=['GET'])
def get_products():
    product = Product.query.all()
    return products_schema.jsonify(product)

@app.route('/products', methods=['POST'])
def add_product():
    try:
        product_data = product_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_product = Product(name = product_data['name'],
                          par_inventory = product_data['par_inventory'],
                          current_inventory = product_data['current_inventory'],
                          price = product_data['price'])
    
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'}), 201


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    try:
        product_data = product_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    product.name = product_data['name']
    product.par_inventory = product_data['par_inventory']
    product.current_inventory = product_data['current_inventory']
    product.price = product_data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully.'}), 400


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully.'})







# Runs app in debug mode to allow for real time updating
if __name__ == "__main__":
    app.run(debug=True)