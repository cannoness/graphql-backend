import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
import os


user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
database_name = os.environ.get("DATABASE_NAME")
GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql+psycopg2://{user}:{password}@localhost/{database_name}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'
