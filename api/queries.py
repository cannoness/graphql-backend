from .models import User
from ariadne import convert_kwargs_to_snake_case


def list_users_resolver(obj, info):
    try:
        users = [user.to_dict() for user in User.query.all()]
        print(users)
        payload = {
            "success": True,
            "posts": users
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def get_user_resolver(obj, info, user_id):
    try:
        users = User.query.get(user_id)
        payload = {
            "success": True,
            "users": users
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
