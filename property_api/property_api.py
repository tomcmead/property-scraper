import flask
import flask_restful
import resources.rightmove

app = flask.Flask(__name__)
api = flask_restful.Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # reduce amount of warnings

@app.before_first_request
def create_tables():
    from database.db import db
    db.init_app(app)
    db.create_all()

api.add_resource(resources.rightmove.Rightmove, '/rightmove')

if __name__ == '__main__':
    app.run(debug=True)