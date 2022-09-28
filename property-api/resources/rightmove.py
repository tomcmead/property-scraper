import flask
import flask_restful

class Location(flask_restful.Resource):
    def __init__(self):
        self.location = {'location': 'empty'}

    def get(self):
        """ returns rightmove location code """
        return self.location
    
    def post(self):
        """ receive """
        location = flask.request.get_json()
        
        if len(location['location'])==7 and location['location'].isalnum():
            self.location = location
            return {'location': self.location}, 201

        return {'ERROR Request Format': 'location: <alphanum code length 7>'}, 400
        
