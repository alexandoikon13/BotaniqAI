from flask import Flask
from dotenv import load_dotenv

load_dotenv()  # This will load the environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

    from .routes import main
    app.register_blueprint(main)

    return app
