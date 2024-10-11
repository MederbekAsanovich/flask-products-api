from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

db_name = 'products.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullalbe=False)
    description = db.Column(db.String(255), nullalbe=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50),nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category
        }
    
@app.route('/products', methods = ['POST'])
def create_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price = data['price'],
        category=data['category']
    )

    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# Get method
@app.route('/products', methods = ['GET'])
def get_products():
    category = request.args.get('category')
    sort = request.args.get('sort')

    query = Product.query

    if category:
        query = query.filter_by(category=category)

    if sort == 'price':
        query = query.order_by(Product.price)

    products = query.all()

    return jsonify([product.to_dict() for product in products])

# Get product by id 
@app.route('/products/<int:id>', methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    if product: 
        return jsonify(product.to_dict())
    
    else:
        return jsonify({
            'error': 'not found'
        }), 404
    
if __name__ == "__main__":
    if not os.path.exists('products.db'):
        db.create_all()
    app.run(debug=True)



