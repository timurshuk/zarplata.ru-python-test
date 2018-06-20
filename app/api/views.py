from flask import jsonify
from . import api
from ..functions.load_vacancies import get_vacancy_by_id
from ..functions.similar_vacancies import get_similar_vacancies


@api.route('/vacancies/similar/<int:vacancy_id>')
def index(vacancy_id):
    # если будет передан id не существующей вакансии будет 500 ошибка
    vacancies = get_similar_vacancies(get_vacancy_by_id(vacancy_id))

    return jsonify({'vacancies': [{'id': vacancy.vacancy_id, 'header': vacancy.header} for vacancy in vacancies]})
