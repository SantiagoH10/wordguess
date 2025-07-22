from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from datetime import datetime
import sys
import traceback

from routes.word2vec import word2vec_bp
from utils.model_manager import ModelManager
from utils.exceptions import ValidationError, ModelError

def create_app():
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__)

    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    # Enable CORS for Express communication
    CORS(app)

    # Setup logging
    setup_logging(app)

    # Initialize model manager
    model_manager = ModelManager()

    # Make model manager available to routes
    app.model_manager = model_manager

    # Register blueprints
    app.register_blueprint(word2vec_bp, url_prefix='/api')

    # Global error handlers
    setup_error_handlers(app)

    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Simple health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'word2vec-ml-service',
            'loaded_models': list(app.model_manager.loaded_models.keys())
        })

    # Root endpoint
    @app.route('/')
    def root():
        """Root endpoint with service information"""
        return jsonify({
            'service': 'Word2Vec ML Service',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'compare': '/api/compare',
                'random': '/api/random',
                'exists': '/api/exists',
                'info': '/api/info'
            },
            'status': 'running'
        })

    return app

def setup_logging(app):
    """Configure application logging"""
    if not app.debug:
        # Production logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s: %(message)s'
        )
    else:
        # Development logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(name)s: %(message)s'
        )

    # Suppress some verbose logs in production
    if not app.debug:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)

def setup_error_handlers(app):
    """Setup global error handlers"""

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Handle custom validation errors"""
        app.logger.warning(f"Validation error: {str(e)}")
        return jsonify({
            'error': 'Validation Error',
            'message': str(e),
            'type': 'validation_error'
        }), 400

    @app.errorhandler(ModelError)
    def handle_model_error(e):
        """Handle model-related errors"""
        app.logger.error(f"Model error: {str(e)}")
        return jsonify({
            'error': 'Model Error',
            'message': str(e),
            'type': 'model_error'
        }), 500

    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested endpoint does not exist',
            'type': 'not_found'
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        """Handle method not allowed errors"""
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for this endpoint',
            'type': 'method_not_allowed'
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(e):
        """Handle internal server errors"""
        app.logger.error(f"Internal error: {str(e)}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'type': 'internal_error'
        }), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        """Handle any unexpected errors"""
        app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Unexpected Error',
            'message': 'An unexpected error occurred',
            'type': 'unexpected_error'
        }), 500

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Development server configuration
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    print(f"Starting Word2Vec ML Service...")
    print(f"Server will run on http://{host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"Health check available at: http://{host}:{port}/health")

    # Pre-load default model for faster first requests (optional)
    try:
        app.logger.info("Pre-loading default model...")
        app.model_manager.get_model('glove-wiki-gigaword-100')
        app.logger.info("Default model loaded successfully")
    except Exception as e:
        app.logger.warning(f"Could not pre-load default model: {e}")

    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True  # Enable threading for better concurrent request handling
    )
