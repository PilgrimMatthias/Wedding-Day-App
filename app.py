# Imports
from flask import Flask
from dotenv import load_dotenv
from config import DevelopmentConfig
from services.photo_service import PhotoService
from services.limiter_service import LimiterService

# Blueprints
from blueprints.main.routes import home_bp
from blueprints.info.routes import info_bp
from blueprints.schedule.routes import schedule_bp
from blueprints.gallery.routes import gallery_bp

# Load environment variables from .env
load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(DevelopmentConfig)

    app.photo_service = PhotoService()
    app.limiter_service = LimiterService()
    app.limiter_service.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(info_bp, url_prefix="/info")
    app.register_blueprint(schedule_bp, url_prefix="/schedule")
    app.register_blueprint(gallery_bp, url_prefix="/gallery")

    return app


app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
