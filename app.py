from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost/dvdrental'
db = SQLAlchemy(app)

@app.route('/')
def greet():
    return 'Hi'

@app.route('/getanycountry')
def get_country():
    from models import Country
    countries = db.session.query(Country).first()
    return countries.country





if __name__ == '__main__':
    app.run()
