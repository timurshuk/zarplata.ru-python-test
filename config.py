class Config(object):
    """
    Common configurations
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/zarplata.ru-test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    API = 'https://api.zp.ru/v1/vacancies/'
    GEO_ID = 826
    VACANCIES_NUMBER = 1000
    VACANCIES_UPLOAD_STEP = 100
    SIMILAR_VACANCIES_NUMBER = 10
