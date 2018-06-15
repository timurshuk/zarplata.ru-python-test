import urllib.parse
import requests
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
from ..models import Vacancy, db
from flask import current_app as app


def make_url(offset):
    parameters = {
        'geo_id': app.config["GEO_ID"],
        'limit': app.config["VACANCIES_UPLOAD_STEP"],
        'offset': offset
    }
    return app.config["API"] + "?" + urllib.parse.urlencode(parameters)


def get_words_of_vacancy(vacancy):
    words = get_word_list(vacancy['header'])
    words += get_word_list(vacancy['description'])
    words += get_word_list(vacancy['requirements'])
    words += get_word_list(vacancy['company']['title'])
    words += get_word_list(vacancy['contact']['address'])

    return words


def get_word_list(text):
    if text:
        ps = PorterStemmer()
        ss = SnowballStemmer("russian")
        pattern = re.compile('<.*?>')
        text = re.sub(pattern, '', text)
        words = re.sub("[^\w]", " ", text).split()
        words = [ps.stem(x) for x in words]
        words = [ss.stem(x) for x in words]

        return words
    else:
        return []


def load_vacancies():
    count_vacancies = db.session.query(Vacancy).count()
    if count_vacancies == 0:
        offset = 0
        while offset < app.config["VACANCIES_NUMBER"]:
            url = make_url(offset)

            data = requests.get(url)
            json_data = data.json()

            vacancies = []
            for vacancy in json_data['vacancies']:
                vacancies.append(Vacancy(
                    vacancy_id=vacancy['id'],
                    header=vacancy['header'],
                    words=' '.join(get_words_of_vacancy(vacancy))
                ))
            db.session.bulk_save_objects(vacancies)
            db.session.commit()

            offset += app.config["VACANCIES_UPLOAD_STEP"]


def get_vacancy_by_id(vacancy_id):
    vacancy = Vacancy.query.filter_by(vacancy_id=vacancy_id).first()
    if vacancy is None:
        data = requests.get(app.config["API"] + str(vacancy_id))
        json_data = data.json()
        for vacancy_object in json_data['vacancies']:
            vacancy = Vacancy(
                vacancy_id=vacancy_object['id'],
                header=vacancy_object['header'],
                words=' '.join(get_words_of_vacancy(vacancy_object))
            )
            db.session.add(vacancy)
            db.session.commit()

    return vacancy

