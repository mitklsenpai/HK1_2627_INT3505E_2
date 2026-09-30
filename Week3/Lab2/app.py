from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

from errors import (ApiProblem, _problem)

# VALIDATION HELPERS
def _body(required, typed=None):
    if not request.is_json:
        raise ApiProblem(
            415,
            "Unsupported Media Type",
            "Content-Type must be application/json",
            type_path="unsupported-media-type"
        )

    data = request.get_json(silent=True)

    if data is None:
        raise ApiProblem(
            400,
            "Malformed JSON",
            "Request body is not valid JSON",
            type_path="malformed-json"
        )

    if not isinstance(data, dict):
        raise ApiProblem(
            400,
            "Invalid Body",
            "Request body must be a JSON object",
            type_path="invalid-body"
        )

    missing = [field for field in required if field not in data]

    if missing:
        raise ApiProblem(
            422,
            "Missing Required Fields",
            f"Missing required field(s): {', '.join(missing)}",
            type_path="missing-fields",
            missing_fields=missing
        )

    for field in (required if typed is None else typed):
        if field in data and not isinstance(data[field], str):
            raise ApiProblem(
                422,
                "Invalid Field Type",
                f"Field '{field}' must be a string",
                type_path="invalid-field-type",
                field=field,
                expected="string"
            )

    return data


def _post_or_404(post_id):
    for post in posts:
        if post["id"] == post_id:
            return post

    raise ApiProblem(
        404,
        "Post Not Found",
        f"Post {post_id} does not exist",
        type_path="post-not-found",
        post_id=post_id
    )

# MOCK DATA
posts = [
    {
        "id": 1,
        "title": "Hello REST API",
        "content": "This is my first post"
    }
]

comments = [
    {
        "id": 1,
        "post_id": 1,
        "content": "Nice post!"
    }
]

tags = [
    {
        "id": 1,
        "post_id": 1,
        "name": "python"
    }
]

followers = [
    {
        "id": 1,
        "post_id": 1,
        "user": "alice"
    }
]

@app.errorhandler(ApiProblem)
def handle_api_problem(error):
    return _problem(
        status=error.status,
        title=error.title,
        detail=error.detail,
        type_path=error.type_path,
        **error.extra
    )

@app.errorhandler(HTTPException)
def handle_http_exception(error):
    return _problem(
        status=error.code,
        title=error.name,
        detail=error.description,
        type_path="http-error"
    )

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app.logger.exception(error)

    return _problem(
        status=500,
        title="Internal Server Error",
        detail="An unexpected error occurred",
        type_path="internal-error"
    )

@app.get("/api/v1/posts")
def get_posts():
    return jsonify(posts), 200


@app.post("/api/v1/posts")
def create_post():
    data = _body(["title", "content"])

    post = {
        "id": max((p["id"] for p in posts), default=0) + 1,
        "title": data["title"],
        "content": data["content"]
    }

    posts.append(post)

    return jsonify(post), 201


@app.get("/api/v1/posts/<int:post_id>")
def get_post(post_id):
    return jsonify(_post_or_404(post_id)), 200

@app.put("/api/v1/posts/<int:post_id>")
def update_post(post_id):

    post = _post_or_404(post_id)
    data = _body(["title", "content"])

    post["title"] = data["title"]
    post["content"] = data["content"]

    return jsonify(post), 200

@app.patch("/api/v1/posts/<int:post_id>")
def patch_post(post_id):

    post = _post_or_404(post_id)
    data = _body([], ["title", "content"])

    fields = [field for field in ("title", "content") if field in data]

    if not fields:
        raise ApiProblem(
            400,
            "Empty Patch Request",
            "Body must contain at least one of: title, content",
            type_path="empty-patch",
            allowed_fields=["title", "content"]
        )

    for field in fields:
        post[field] = data[field]

    return jsonify(post), 200

@app.delete("/api/v1/posts/<int:post_id>")
def delete_post(post_id):

    post = _post_or_404(post_id)

    posts.remove(post)
    comments[:] = [c for c in comments if c["post_id"] != post_id]
    tags[:] = [t for t in tags if t["post_id"] != post_id]
    followers[:] = [f for f in followers if f["post_id"] != post_id]

    return "", 204


@app.get("/api/v1/posts/<int:post_id>/comments")
def get_comments(post_id):

    _post_or_404(post_id)

    result = [
        comment
        for comment in comments
        if comment["post_id"] == post_id
    ]

    return jsonify(result), 200


@app.post("/api/v1/posts/<int:post_id>/comments")
def create_comment(post_id):

    _post_or_404(post_id)
    data = _body(["content"])

    comment = {
        "id": max((c["id"] for c in comments), default=0) + 1,
        "post_id": post_id,
        "content": data["content"]
    }

    comments.append(comment)

    return jsonify(comment), 201

@app.get("/api/v1/posts/<int:post_id>/tags")
def get_tags(post_id):

    _post_or_404(post_id)

    result = [
        tag
        for tag in tags
        if tag["post_id"] == post_id
    ]

    return jsonify(result), 200

@app.post("/api/v1/posts/<int:post_id>/tags")
def create_tag(post_id):

    _post_or_404(post_id)
    data = _body(["name"])

    for tag in tags:
        if tag["post_id"] == post_id and tag["name"].lower() == data["name"].lower():
            raise ApiProblem(
                409,
                "Tag Already Exists",
                f"Tag '{data['name']}' is already applied to post {post_id}",
                type_path="duplicate-tag",
                post_id=post_id,
                name=data["name"]
            )

    tag = {
        "id": max((t["id"] for t in tags), default=0) + 1,
        "post_id": post_id,
        "name": data["name"]
    }

    tags.append(tag)

    return jsonify(tag), 201

@app.get("/api/v1/posts/<int:post_id>/followers")
def get_followers(post_id):

    _post_or_404(post_id)

    result = [
        follower
        for follower in followers
        if follower["post_id"] == post_id
    ]

    return jsonify(result), 200


@app.post("/api/v1/posts/<int:post_id>/followers")
def create_follower(post_id):

    _post_or_404(post_id)
    data = _body(["user"])

    for follower in followers:
        if follower["post_id"] == post_id and follower["user"].lower() == data["user"].lower():
            raise ApiProblem(
                409,
                "Follower Already Exists",
                f"User '{data['user']}' already follows post {post_id}",
                type_path="duplicate-follower",
                post_id=post_id,
                user=data["user"]
            )

    follower = {
        "id": max((f["id"] for f in followers), default=0) + 1,
        "post_id": post_id,
        "user": data["user"]
    }

    followers.append(follower)

    return jsonify(follower), 201


if __name__ == "__main__":
    app.run(port = 5000)