import flask
import flask_restful
import resources.rightmove

app = flask.Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(resources.rightmove.Location, '/location')
api.add_resource(resources.rightmove.RightmoveScraper, '/rightmove')

if __name__ == '__main__':
    app.run(debug=True)