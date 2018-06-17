from subprocess import Popen
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import current_app as app
from ..models import Vacancy,db


def set_tfidf_vectors(all_vacancies=None):
    if all_vacancies is None:
        all_vacancies = Vacancy.query.all()

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform([x.words for x in all_vacancies])
    update_vectors_of_vacancies(all_vacancies, tfidf_matrix_train.toarray())


def update_vectors_of_vacancies(all_vacancies, npm_tfidf):
    for i, vacancy in enumerate(all_vacancies):
        vacancy.vector = ' '.join([str(x) for x in npm_tfidf[i]])
    db.session.commit()


def get_similar_vacancies(check_vacancy):
    all_vacancies = Vacancy.query.filter(Vacancy.vacancy_id != check_vacancy.vacancy_id).all()
    if check_vacancy.vector is not None:
        train_set = [[float(x) for x in vacancy.vector.split()] for vacancy in all_vacancies]
        similarity_list = cosine_similarity([[float(x) for x in check_vacancy.vector.split()]], train_set)
        for i, value in enumerate(similarity_list[0].tolist()):
            all_vacancies[i].similarity_index = value
    else:
        train_set = [check_vacancy.words] + [x.words for x in all_vacancies]
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)
        similarity_list = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)
        update_vectors_of_vacancies([check_vacancy] + all_vacancies, tfidf_matrix_train.toarray())

        for i, value in enumerate(similarity_list[0][1:].tolist()):
            all_vacancies[i].similarity_index = value

    all_vacancies = sorted(all_vacancies, key=lambda student: student.similarity_index, reverse=True)

    return all_vacancies[:app.config["SIMILAR_VACANCIES_NUMBER"]]
