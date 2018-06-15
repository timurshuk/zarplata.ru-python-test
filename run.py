from app import create_app, db, cli
from app.models import Vacancy

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Vacancy': Vacancy}


if __name__ == '__main__':
    app.run()
