import os
from flask import Flask
from flask_cors import CORS
from config import config_selector
from app.database import initialize_database
from app.routes import api_interface

def initialize_app(config_name: str = None) -> Flask:
    app = Flask(__name__, template_folder="templates")

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "")
    selected_config = config_selector.get(config_name, config_selector["development"])
    app.config.from_object(selected_config)

    
    CORS(
        app,
        origins=app.config.get("CORS_ALLOWED_ORIGINS", "*"),
        methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        credentials = True,
    )

    with app.app_context():
        initialize_database(app)

    
    app.register_blueprint(api_arayuzu, url_prefix="/api")

    @app.route("/health")
    def saglik_kontrolu():
        """Sunucunun Ayakta Olup Olmadığını Bildiren Uç Nokta (Health Check)."""
        from flask import jsonify
        return jsonify({"durum": "aktif", "servis": "Akıllı Satış AI"}), 200

    return app
