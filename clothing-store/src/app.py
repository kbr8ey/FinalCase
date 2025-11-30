import logging
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app with static files
CWD = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.abspath(os.path.join(CWD, '..'))
app = Flask(__name__, static_folder='assets', static_url_path='/assets')
import os
# Sample product data with image URLs

# Always register /home.html route
@app.route('/home.html', methods=['GET'])
def serve_home():
    """Serve home.html from project root"""
    return send_from_directory(APP_ROOT, 'home.html')
CORS(app)

# Sample product data with image URLs
PRODUCTS = {
    1: {
        "id": 1,
        "name": "T-Shirt",
        "price": 19.99,
        "category": "tops",
        "size": "M",
        "color": "blue",
        "image_url": "/assets/images/t-shirt.jpg"
    },
    2: {
        "id": 2,
        "name": "Jeans",
        "price": 49.99,
        "category": "bottoms",
        "size": "32",
        "color": "dark blue",
        "image_url": "/assets/images/jeans.jpg"
    },
    3: {
        "id": 3,
        "name": "Jacket",
        "price": 89.99,
        "category": "outerwear",
        "size": "L",
        "color": "black",
        "image_url": "/assets/images/jacket.jpg"
    },
    4: {
        "id": 4,
        "name": "Sneakers",
        "price": 79.99,
        "category": "shoes",
        "size": "10",
        "color": "white",
        "image_url": "/assets/images/sneakers.jpg"
    },
}

# Cart storage (in-memory for demo)
carts = {}


@app.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    logger.info("Fetching all products")
    return jsonify(list(PRODUCTS.values())), 200


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    logger.info(f"Fetching product with ID: {product_id}")
    
    product = PRODUCTS.get(product_id)
    if not product:
        logger.warning(f"Product not found: {product_id}")
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(product), 200


@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add product to cart"""
    data = request.get_json()
    
    if not data or 'product_id' not in data or 'user_id' not in data:
        logger.warning("Invalid cart add request: missing product_id or user_id")
        return jsonify({"error": "Missing product_id or user_id"}), 400
    
    product_id = data.get('product_id')
    user_id = data.get('user_id')
    quantity = data.get('quantity', 1)
    
    # Validate product exists
    if product_id not in PRODUCTS:
        logger.warning(f"Product not found in add_to_cart: {product_id}")
        return jsonify({"error": "Product not found"}), 404
    
    # Initialize cart for user if not exists
    if user_id not in carts:
        carts[user_id] = []
    
    # Add product to cart
    product = PRODUCTS[product_id]
    cart_item = {
        "product_id": product_id,
        "name": product["name"],
        "price": product["price"],
        "quantity": quantity
    }
    
    carts[user_id].append(cart_item)
    logger.info(f"Added product {product_id} to cart for user {user_id}")
    
    return jsonify({
        "message": "Product added to cart",
        "cart": carts[user_id]
    }), 201


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info("Health check")
    return jsonify({"status": "healthy"}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {error}")
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    logger.info("Starting Clothing Store API")
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
