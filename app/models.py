from app import db


class Vacancy(db.Model):
    """
    Create an Vacancy table
    """

    __tablename__ = 'vacancy'

    id = db.Column(db.Integer, primary_key=True)
    vacancy_id = db.Column(db.Integer, index=True, unique=True)
    header = db.Column(db.String(255), index=True)
    words = db.Column(db.Text())
    vector = db.Column(db.Text())
    similarity_index = 0

    def __repr__(self):
        return '<Vacancy %d>' % self.id
