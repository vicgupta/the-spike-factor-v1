from flask import render_template, redirect, url_for, current_app
from flask_login import current_user

def register_routes(app):
    @app.route('/')
    @app.route('/index')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return render_template('index.html', title='The Spike Factor')