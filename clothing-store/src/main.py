"""Main entry point for the clothing store application"""
import os
from src.app import app


if __name__ == "__main__":
    # Force Flask to use the same port every time
    port = 8080  
    app.run(host="0.0.0.0", port=port)
