import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure logging
    configure_logging(app)

    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    from app.assessment import bp as assessment_bp
    app.register_blueprint(assessment_bp, url_prefix='/assessment')

    from app.reports import bp as reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')

    from app.payment import bp as payment_bp
    app.register_blueprint(payment_bp, url_prefix='/payment')

    from app import models
    from app.routes import register_routes
    register_routes(app)

    return app

def configure_logging(app):
    """Configure application logging with detailed Stripe payment logging"""
    # Get log level from environment or default to INFO
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format='%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler('logs/app.log', mode='a')  # File output
        ]
    )

    # Configure Stripe payment logger specifically
    stripe_logger = logging.getLogger('app.payment')
    stripe_logger.setLevel(logging.DEBUG)

    # Create a separate file handler for Stripe payments
    stripe_handler = logging.FileHandler('logs/stripe_payments.log', mode='a')
    stripe_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s:%(lineno)d %(funcName)s() %(message)s'
    )
    stripe_handler.setFormatter(stripe_formatter)
    stripe_logger.addHandler(stripe_handler)

    # Configure Stripe library logging
    stripe_lib_logger = logging.getLogger('stripe')
    stripe_lib_logger.setLevel(logging.DEBUG)
    stripe_lib_handler = logging.FileHandler('logs/stripe_api.log', mode='a')
    stripe_lib_handler.setFormatter(stripe_formatter)
    stripe_lib_logger.addHandler(stripe_lib_handler)

    app.logger.info('Logging configured successfully')
    app.logger.info(f'Application log level: {log_level}')
    app.logger.info('Stripe payment logging enabled with DEBUG level')