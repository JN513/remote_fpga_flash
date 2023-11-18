import os
import json
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    jsonify,
    send_from_directory,
    abort,
)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"fs", "bin", "elf"}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def flash_board(file_path, board, busdev):

    r = os.system(
        f"/home/julio/eda/oss-cad-suite/bin/openFPGALoader -f -b {board} {file_path} --busdev-num {busdev} > out.txt")

    print(
        f"openFPGALoader -f -b {board} {file_path} -busdev-num {busdev} > out.txt")

    data = open("out.txt", "r")

    content = ""

    for line in data.readlines():
        content += line

    data.close()
    os.remove("out.txt")
    if 0:
        os.remove(file_path)

    return r, content


@app.route("/flash_9k", methods=["POST"])
def flash_route_9k():
    board = "tangnano9k"
    busdev = "01:046"

    if not "file" in request.files:
        return jsonify({"success": False, "error": "Arquivo não enviado"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    if "/" in file.filename:
        return jsonify({"success": False, "error": "no subdirectories allowed"}), 400

    filename = ""

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
    else:
        return jsonify({"success": False, "error": "No selected file"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    r, content = flash_board(file_path, board, busdev)

    if r != 0:
        return jsonify({"success": False, "filename": filename, "message": content, "execution_code": r}), 400
    else:
        return jsonify({"success": False, "filename": filename, "message": content, "execution_code": r}), 201


@app.route("/flash_20k", methods=["POST"])
def flash_route_20k():
    board = "tangnano20k"
    busdev = "01:045"

    if not "file" in request.files:
        return jsonify({"success": False, "error": "Arquivo não enviado"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    if "/" in file.filename:
        return jsonify({"success": False, "error": "no subdirectories allowed"}), 400

    filename = ""

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
    else:
        return jsonify({"success": False, "error": "No selected file"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    r, content = flash_board(file_path, board, busdev)

    if r != 0:
        return jsonify({"success": False, "filename": filename, "message": content, "execution_code": r}), 400
    else:
        return jsonify({"success": False, "filename": filename, "message": content, "execution_code": r}), 201


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(host="0.0.0.0", port=8000)
