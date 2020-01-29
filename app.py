from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import ActorMovies, GetCountry,Actors
from flask_restful import Resource, Api,reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost/dvdrental'
db = SQLAlchemy(app)
api = Api(app)


class Country(Resource):

    def get(self):
        countries = db.session.execute("SELECT country FROM country " +
                                       "LIMIT 10")
        country_list = []
        for item in countries:
            country = GetCountry(item[0])
            country_list.append(country.__dict__)
        return country_list


api.add_resource(Country, '/country')


class Actor(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('first_name', type=str, required='True', help="This field cannot be empty")
    parser.add_argument('last_name', type=str, required='True', help="This field cannot be empty")

    def get(self):
        actors = db.session.execute("SELECT first_name,last_name FROM actor LIMIT 10")
        actors_list = []
        for item in actors:
            actor = Actors(item[0],item[1])
            actors_list.append(actor.__dict__)
        return actors_list

    def post(self):
        request_data = Actor.parser.parse_args()
        db.session.execute(
            "INSERT INTO actor(first_name, last_name, last_update) VALUES (:fn, :ln, current_date)",
            {"fn": request_data['first_name'], "ln": request_data['last_name']})
        db.session.commit()
        return request_data


api.add_resource(Actor, '/actor')


@app.route('/top_ten_actors')
def getTopTenActors():
    result = db.session.execute("SELECT first_name,last_name ,count(DISTINCT film_id) FROM actor " +
                                "INNER JOIN film_actor ON actor.actor_id=film_actor.actor_id " +
                                "GROUP BY first_name,last_name " +
                                "ORDER BY count(DISTINCT film_id) DESC " +
                                "LIMIT 10")
    output = []
    for item in result:
        actor_movies = ActorMovies(item[0], item[1], item[2])
        output.append(actor_movies.__dict__)
    return output


if __name__ == '__main__':
    app.debug = True
    app.run()
