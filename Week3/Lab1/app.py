from flask import Flask, request, jsonify

app = Flask(__name__)

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


@app.get("/api/v1/posts")
def get_posts():
    return jsonify(posts), 200


@app.post("/api/v1/posts")
def create_post():
    data = request.get_json()

    post = {
        "id": len(posts) + 1,
        "title": data["title"],
        "content": data["content"]
    }

    posts.append(post)

    return jsonify(post), 201


@app.get("/api/v1/posts/<int:post_id>")
def get_post(post_id):

    for post in posts:
        if post["id"] == post_id:
            return jsonify(post), 200

    return jsonify({
        "error": "Post not found"
    }), 404

@app.put("/api/v1/posts/<int:post_id>")
def update_post(post_id):

    data = request.get_json()

    for post in posts:
        if post["id"] == post_id:

            post["title"] = data["title"]
            post["content"] = data["content"]

            return jsonify(post), 200

    return jsonify({
        "error": "Post not found"
    }), 404

@app.patch("/api/v1/posts/<int:post_id>")
def patch_post(post_id):

    data = request.get_json()

    for post in posts:
        if post["id"] == post_id:

            if "title" in data:
                post["title"] = data["title"]

            if "content" in data:
                post["content"] = data["content"]

            return jsonify(post), 200

    return jsonify({
        "error": "Post not found"
    }), 404

@app.delete("/api/v1/posts/<int:post_id>")
def delete_post(post_id):

    for post in posts:
        if post["id"] == post_id:

            posts.remove(post)

            return "", 204

    return jsonify({
        "error": "Post not found"
    }), 404


@app.get("/api/v1/posts/<int:post_id>/comments")
def get_comments(post_id):

    result = [
        comment
        for comment in comments
        if comment["post_id"] == post_id
    ]

    return jsonify(result), 200


@app.post("/api/v1/posts/<int:post_id>/comments")
def create_comment(post_id):

    data = request.get_json()

    comment = {
        "id": len(comments) + 1,
        "post_id": post_id,
        "content": data["content"]
    }

    comments.append(comment)

    return jsonify(comment), 201

@app.get("/api/v1/posts/<int:post_id>/tags")
def get_tags(post_id):

    result = [
        tag
        for tag in tags
        if tag["post_id"] == post_id
    ]

    return jsonify(result), 200

@app.post("/api/v1/posts/<int:post_id>/tags")
def create_tag(post_id):

    data = request.get_json()

    tag = {
        "id": len(tags) + 1,
        "post_id": post_id,
        "name": data["name"]
    }

    tags.append(tag)

    return jsonify(tag), 201

@app.get("/api/v1/posts/<int:post_id>/followers")
def get_followers(post_id):

    result = [
        follower
        for follower in followers
        if follower["post_id"] == post_id
    ]

    return jsonify(result), 200


@app.post("/api/v1/posts/<int:post_id>/followers")
def create_follower(post_id):

    data = request.get_json()

    follower = {
        "id": len(followers) + 1,
        "post_id": post_id,
        "user": data["user"]
    }

    followers.append(follower)

    return jsonify(follower), 201


if __name__ == "__main__":
    app.run(debug=True, port = 5000)