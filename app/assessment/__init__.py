from flask import Blueprint

bp = Blueprint('assessment', __name__)

from app.assessment import routes