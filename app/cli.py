from .functions.load_vacancies import load_vacancies


def register(app):
    @app.cli.command('load-vacancies')
    def load():
        """Load vacancies."""
        load_vacancies()
