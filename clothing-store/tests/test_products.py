"""Tests for the clothing store API"""
import sys
import os
import pytest
import json

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestProducts:
    """Test cases for product endpoints"""

    def test_get_products_returns_200(self, client):
        """Test that GET /products returns 200 status code"""
        response = client.get('/products')
        assert response.status_code == 200

    def test_get_products_returns_json_list(self, client):
        """Test that GET /products returns a JSON list"""
        response = client.get('/products')
        data = response.get_json()
        
        # Check that response is a list
        assert isinstance(data, list), "Response should be a list"
        
        # Check that list is not empty
        assert len(data) > 0, "Product list should not be empty"

    def test_get_products_json_structure(self, client):
        """Test that products in list have expected structure"""
        response = client.get('/products')
        data = response.get_json()
        
        # Check first product structure
        product = data[0]
        required_fields = ['id', 'name', 'category', 'price', 'size', 'color', 'image_url']
        
        for field in required_fields:
            assert field in product, f"Product should have '{field}' field"

    def test_get_products_content_type(self, client):
        """Test that response has correct content type"""
        response = client.get('/products')
        assert response.content_type == 'application/json'

    def test_get_single_product_returns_200(self, client):
        """Test that GET /products/<id> returns 200 for valid product"""
        response = client.get('/products/1')
        assert response.status_code == 200

    def test_get_single_product_returns_json(self, client):
        """Test that GET /products/<id> returns JSON product"""
        response = client.get('/products/1')
        data = response.get_json()
        
        assert isinstance(data, dict), "Response should be a dictionary"
        assert data['id'] == 1, "Product ID should match request"

    def test_get_invalid_product_returns_404(self, client):
        """Test that GET /products/<id> returns 404 for invalid product"""
        response = client.get('/products/9999')
        assert response.status_code == 404

    def test_health_check_returns_200(self, client):
        """Test that health check endpoint is working"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_add_to_cart_success(self, client):
        """Test successful cart addition"""
        response = client.post('/cart/add',
            json={
                'user_id': 'test_user',
                'product_id': 1,
                'quantity': 2
            },
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'cart' in data
        assert len(data['cart']) > 0

    def test_add_to_cart_missing_user_id(self, client):
        """Test cart addition with missing user_id"""
        response = client.post('/cart/add',
            json={
                'product_id': 1,
                'quantity': 1
            },
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_add_to_cart_invalid_product(self, client):
        """Test cart addition with invalid product"""
        response = client.post('/cart/add',
            json={
                'user_id': 'test_user',
                'product_id': 9999,
                'quantity': 1
            },
            content_type='application/json'
        )
        assert response.status_code == 404

    def test_products_data_integrity(self, client):
        """Test that all products have valid data"""
        response = client.get('/products')
        products = response.get_json()
        
        for product in products:
            # Validate price is positive
            assert product['price'] > 0, f"Product {product['id']} has invalid price"
            
            # Validate required text fields
            assert len(product['name']) > 0, f"Product {product['id']} has empty name"
            assert len(product['category']) > 0, f"Product {product['id']} has empty category"
            
            # Validate image_url format
            if product['image_url']:
                assert isinstance(product['image_url'], str), "image_url must be string"


class TestAPI:
    """Integration tests for API as a whole"""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present"""
        response = client.get('/products')
        assert 'Access-Control-Allow-Origin' in response.headers

    def test_error_handling_404(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent')
        assert response.status_code == 404

    def test_json_response_format(self, client):
        """Test all responses are valid JSON"""
        endpoints = ['/products', '/health']
        for endpoint in endpoints:
            response = client.get(endpoint)
            try:
                json.loads(response.data)
            except json.JSONDecodeError:
                pytest.fail(f"Response from {endpoint} is not valid JSON")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
