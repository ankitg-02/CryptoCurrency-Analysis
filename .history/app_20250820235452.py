import os
from flask import Flask, render_template
from src.models.user import db, User
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import webbrowser
from threading import Timer

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    bcrypt = Bcrypt(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Import and register blueprints
    from src.routes import main
    app.register_blueprint(main)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='localhost',  # Changed from 0.0.0.0 for development
        port=5000,
        debug=True,
        use_reloader=True
    )