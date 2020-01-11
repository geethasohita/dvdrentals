from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def greet():
    return 'Hi'


if __name__ == '__main__':
    app.run()
