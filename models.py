from app import db


class Country(db.Model):
    __tablename__ = "country"
    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String)

    def __init__(self, country):
        self.country = country

    def __repr__(self):
        return '<country %r>' % self.country
