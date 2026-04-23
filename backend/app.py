from flask import Flask, jsonify
from flask_cors import CORS
# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from config import Config
from routes.parse_routes import parse_bp
from routes.metrics_routes import metrics_bp
from routes.analysis_routes import analysis_bp
from routes.report_routes import report_bp


def create_app() -> Flask:

    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS with allowed origins
    cors_origins = Config.get_cors_origins()
    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600,
        }
    })
    
    Config.init_upload_folder()

    app.register_blueprint(parse_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(report_bp)

    _register_base_routes(app)

    return app


def _register_base_routes(app: Flask) -> None:

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "Welcome to migration stats"
        }), 200

    @app.errorhandler(413)
    def file_too_large(error):
        max_mb = Config.MAX_CONTENT_LENGTH // (1024 * 1024)
        return jsonify({
            "error": f"File too large. Maximum allowed size is {max_mb} MB.",
        }), 413

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error."}), 500


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
