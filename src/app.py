from flask import Flask, render_template, request, redirect, send_from_directory
import os
from shellcode import gen_shellcode
import secrets
from functools import wraps
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
AUTHKEY = os.getenv("AUTHKEY")
SHELLCODE_DIRECTORY = os.getenv("SHELLCODE_DIRECTORY")

file_dict = {}


def verification_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(request.cookies)
        if request.cookies.get("whoareyou", "a") != AUTHKEY:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def homepage():
    return "hello world!"


@app.route("/scg")
@verification_required
def mainpage():
    return render_template("index.html")


@app.route("/api/g", methods=["POST"])
def generate_shellcode():
    cmd = request.form["cmd"]
    args = request.form["args"]
    shellcode_path = gen_shellcode(cmd, args)
    if os.path.exists(shellcode_path):
        secret_code = secrets.token_hex(24)
        file_dict[secret_code] = shellcode_path
        return f"{request.host_url}api/d/{secret_code}"
    else:
        return "something went wrong."


@app.route("/api/d/<id>")
def download_shellcode(id):
    shellcode_id = id
    shellcode_path = file_dict[shellcode_id]
    shellcode_name = shellcode_path.split("\\")[-1]
    print(shellcode_name)
    if os.path.exists(shellcode_path):
        return send_from_directory(
            directory=SHELLCODE_DIRECTORY, path=shellcode_name, as_attachment=True
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13371)
