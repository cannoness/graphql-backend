from datetime import date

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import User


@convert_kwargs_to_snake_case
def create_user_resolver(obj, info, unique_id, username, email, profile_pic):
    try:
        today = date.today()
        user = User(
            id=unique_id,
            username=username, created_at=today.strftime("%b-%d-%Y"),
            last_updated=today.strftime("%b-%d-%Y"), email=email, profile_pic=profile_pic
        )
        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload


@convert_kwargs_to_snake_case
def update_user_resolver(obj, info, user_id, username, email, picture):
    try:
        user = User.query.get(user_id)
        today = date.today()
        if user:
            user.username = username
            user.email = email
            user.profile_pic = picture
            user.last_updated = today.strftime("%b-%d-%Y")
        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user.to_dict()
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"item matching id {user_id} not found"]
        }

    return payload


@convert_kwargs_to_snake_case
def delete_user_resolver(obj, info, user_id):
    try:
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        payload = {"success": True, "user": user.to_dict()}

    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }

    return payload
