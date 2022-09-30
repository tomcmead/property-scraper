from database.db import db
from sqlalchemy_utils import JSONType

class RightmoveModel(db.Model):
    __tablename__ = 'rightmove'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    location = db.Column(db.String(7))
    links = db.Column(JSONType)

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def save_to_db(self):  
        """ upsert model data entry to database """
        db.session.add(self)
        db.session.commit()

    def json(self):
        """ model entry data """
        return {'name': self.name, 'location': self.location, 'links': self.links}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # simple top 1 select

    def delete_from_db(self):
        """ remove model data entry from database """
        db.session.delete(self)
        db.session.commit()
