import os
import logging
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(APP_ROOT, 'src', 'data', 'products.json')
app = Flask(__name__, static_folder='assets', static_url_path='/assets')
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load products from products.json
def load_products():
    try:
        with open(DATA_PATH, 'r') as f:
            products = json.load(f)
        # Convert list to dict by id for compatibility
        return {p['id']: p for p in products}
    except Exception as e:
        logger.error(f"Failed to load products.json: {e}")
        return {}

# Serve home.html from project root
@app.route('/home.html', methods=['GET'])
def serve_home():
    return send_from_directory(APP_ROOT, 'home.html')

# --- Your API routes and error handlers below ---
# (Keep your PRODUCTS, /products, /products/<id>, /cart/add, /health, error handlers, etc.)

# Cart storage (in-memory for demo)
carts = {}


@app.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    products = load_products()
    return jsonify(list(products.values())), 200


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    products = load_products()
    product = products.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add product to cart with size and color"""
    data = request.get_json()

    if not data or 'product_id' not in data or 'user_id' not in data:
        return jsonify({"error": "Missing product_id or user_id"}), 400

    product_id = data.get('product_id')
    user_id = data.get('user_id')
    quantity = data.get('quantity', 1)
    size = data.get('size')
    color = data.get('color')

    products = load_products()
    # Validate product exists
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    # Validate size
    product = products[product_id]
    if size and size not in product.get('sizes', []):
        return jsonify({"error": "Invalid size for product"}), 400

    # Validate color
    if color and color not in product.get('colors', []):
        return jsonify({"error": "Invalid color for product"}), 400

    # Initialize cart for user if not exists
    if user_id not in carts:
        carts[user_id] = []

    # Add product to cart
    cart_item = {
        "product_id": product_id,
        "name": product["name"],
        "price": product["price"],
        "quantity": quantity,
        "size": size,
        "color": color
    }

    carts[user_id].append(cart_item)

    return jsonify({
        "message": "Product added to cart",
        "cart": carts[user_id]
    }), 201


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    port = 8080
    #int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
