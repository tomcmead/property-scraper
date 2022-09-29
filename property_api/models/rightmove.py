from database.db import db

class RightmoveModel(db.Model):
    __tablename__ = 'rightmove'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(7))

    def __init__(self, location):
        self.location = location

    def save_to_db(self):  
        """ upsert model data entry to database """
        db.session.add(self)
        db.session.commit()

    def json(self):
        """ model entry data """
        return {'location': self.location}

    def delete_from_db(self):
        """ remove model data entry from database """
        db.session.delete(self)
        db.session.commit()
