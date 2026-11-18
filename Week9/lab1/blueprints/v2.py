from flask import Blueprint, request, url_for

from .users_data import create_user, get_user


bp = Blueprint("v2", __name__, url_prefix="/users")


@bp.get("/<int:uid>")
def get(uid):
    user = get_user(uid)
    if user is None:
        return {"error": "nf"}, 404
    return {"id": uid, **user}


@bp.post("")
def create():
    if not request.is_json:
        return {"error": "Content-Type must be application/json"}, 415
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return {"error": "JSON body must be an object"}, 400
    fields = ("first_name", "last_name", "email")
    if any(not isinstance(body.get(key), str) or not body[key].strip() for key in fields):
        return {"error": "first_name, last_name and email must be non-empty strings"}, 400
    user = create_user(**{key: body[key].strip() for key in fields})
    return user, 201, {"Location": url_for("v2.get", uid=user["id"])}
