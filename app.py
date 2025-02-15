from flask import (
    Flask,
    request,
    jsonify,
    Response,
    render_template,
    session,
    send_file,
    redirect,
    url_for,
    flash,
)
import requests
from pymongo import MongoClient
import gridfs
import logging
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["image_db"]
fs = gridfs.GridFS(db)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

log = logging.getLogger("werkzeug")


class HideImageRouteFilter(logging.Filter):
    def filter(self, record):
        return not ("/image" in record.getMessage() and "GET" in record.getMessage())


log.addFilter(HideImageRouteFilter())


@app.route("/image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    file = request.files["file"]
    tags = request.form.get("tags")
    password = request.form.get("password")
    tags = [tag.strip() for tag in tags.split(",")] + ["cat"]
    tags = list(set(tags))
    file_id = fs.put(
        file, filename=file.filename, metadata={"tags": tags, "password": password}
    )

    return jsonify({"message": "File uploaded successfully!", "file_id": str(file_id)})


@app.route("/image", methods=["PUT"])
def update_image():
    if "file" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    file = request.files["file"]

    file_data = fs.find_one({"filename": file.filename})
    if file_data:
        fs.delete(file_data._id)

    file_id = fs.put(file, filename=file.filename)
    return jsonify({"message": "File uploaded successfully!", "file_id": str(file_id)})


@app.route("/image/<filename>", methods=["DELETE"])
def delete_image(filename):
    file_data = fs.find_one({"filename": filename})
    if not file_data:
        return jsonify({"error": "File not found"}), 404

    password = request.json.get("password")

    if not password or password != file_data.metadata.get("password"):
        return jsonify({"error": "Password does not match"}), 403

    fs.delete(file_data._id)
    return jsonify(
        {"success": True, "message": f"File {filename} deleted successfully!"}
    )


@app.route("/image/<filename>", methods=["GET"])
def get_images(filename):
    file_data = fs.find_one({"filename": filename})
    if not file_data:
        return jsonify({"error": "File not found"}), 404

    return Response(file_data.read(), mimetype="image/jpeg")


@app.route("/image/<filename>/download")
def download_image(filename):
    file_data = fs.find_one({"filename": filename})
    if not file_data:
        return jsonify({"error": "File not found"}), 404

    return send_file(
        BytesIO(file_data.read()),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=filename,
    )


@app.route("/image/<filename>/like", methods=["POST"])
def like_image(filename):
    file_data = db["fs.files"].find_one({"filename": filename})
    if not file_data:
        return jsonify({"error": "File not found"}), 404

    current_likes = file_data.get("like", 0)

    db["fs.files"].update_one(
        {"filename": filename}, {"$set": {"like": current_likes + 1}}
    )
    session[f"{filename}-like"] = "liked"

    return jsonify({"success": True, "filename": filename, "likes": current_likes + 1})


@app.route("/image/<filename>/dislike", methods=["POST"])
def dislike_image(filename):
    file_data = db["fs.files"].find_one({"filename": filename})
    if not file_data:
        return jsonify({"error": "File not found"}), 404

    current_likes = file_data.get("like", 0)

    db["fs.files"].update_one(
        {"filename": filename}, {"$set": {"like": current_likes - 1}}
    )
    session.pop(f"{filename}-like")

    return jsonify({"success": True, "filename": filename, "likes": current_likes + 1})


@app.route("/", methods=["GET", "POST"])
@app.route("/search/<tag>")
def home(tag=None):
    if request.method == "GET":
        query = {"metadata.tags": {"$in": [tag]}} if tag else {}
        file_data = list(db["fs.files"].find(query))
        length = len(file_data)
        file_data.sort(key=lambda x: x.get("like", 0), reverse=True)
        if file_data:
            images = [[] for _ in range(4)]
            for index, image in enumerate(file_data):
                if session.get(f"{image["filename"]}-like"):
                    image["liked"] = True
                else:
                    image["liked"] = False
                images[index % 4].append(image)
        else:
            images = None
        return render_template("index.html", images=images, length=length, tag=tag)
    else:
        form_data = request.form
        files = request.files

        if not form_data:
            flash("Oops, something is wrong!", "error")
        if not files:
            flash("Oops, something is wrong!", "error")

        file = files.get("file")
        tags = form_data.get("tags")
        password = form_data.get("password")

        response = requests.post(
            url_for("upload_image", _external=True),
            files={"file": (file.filename, file, "image/jpeg")},
            data={"tags": tags, "password": password},
        )
        if response.status_code != 200:
            flash("Oops, something is wrong!", "error")

        return redirect(url_for("home"))
