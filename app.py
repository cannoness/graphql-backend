import os

from flask_login import LoginManager

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify, Flask
from oauthlib.oauth2 import WebApplicationClient

from api.queries import list_posts_resolver, get_post_resolver, get_user_resolver
from api.mutations import create_post_resolver, update_post_resolver, delete_post_resolver


query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listPosts", list_posts_resolver)
query.set_field("getPost", get_post_resolver)
query.set_field("getUser", get_user_resolver)

mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


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
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return get_user_resolver(user_id)
