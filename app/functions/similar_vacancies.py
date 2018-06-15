from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import current_app as app
from ..models import Vacancy


def get_similar_vacancies(check_vacancy):
    all_vacancies = Vacancy.query.filter(Vacancy.vacancy_id != check_vacancy.vacancy_id).all()
    train_set = [check_vacancy.words] + [x.words for x in all_vacancies]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)
    similarity_list = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)

    for i, value in enumerate(similarity_list[0][1:].tolist()):
        all_vacancies[i].similarity_index = value

    all_vacancies = sorted(all_vacancies, key=lambda student: student.similarity_index, reverse=True)

    return all_vacancies[:app.config["SIMILAR_VACANCIES_NUMBER"]]
