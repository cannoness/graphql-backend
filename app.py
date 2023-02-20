import os
from api import app

from flask_login import LoginManager

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify, Flask, redirect
from oauthlib.oauth2 import WebApplicationClient

import api
from api.queries import get_user_resolver, list_users_resolver
from api.mutations import create_user_resolver, update_user_resolver, delete_user_resolver


query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listUsers", list_users_resolver)
query.set_field("getUser", get_user_resolver)

mutation.set_field("createUser", create_user_resolver)
mutation.set_field("updateUser", update_user_resolver)
mutation.set_field("deleteUser", delete_user_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")


# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return api.queries.User.query.get(user_id)


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = api.get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


if __name__ == "__main__":
    app.run()
