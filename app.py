from app import create_app, db
from app.models import User, Assessment, Response, Report

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Assessment': Assessment, 'Response': Response, 'Report': Report}

if __name__ == '__main__':
    app.run(debug=True)