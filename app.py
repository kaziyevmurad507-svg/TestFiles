from flask import Flask, request, Response, render_template
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


def generate_file(size):
    chunk_size = 1024 * 1024
    sent = 0

    while sent < size:
        remaining = size - sent
        chunk = min(chunk_size, remaining)

        yield os.urandom(chunk)

        sent += chunk


@app.route("/download")
def download():

    size = int(request.args.get("size"))
    unit = request.args.get("unit")

    if unit == "GB":
        size_bytes = size * 1024 * 1024 * 1024
    elif unit == "MB":
        size_bytes = size * 1024 * 1024
    elif unit == "KB":
        size_bytes = size * 1024
    else:
        size_bytes = size * 1024 * 1024

    headers = {
        "Content-Disposition": f"attachment; filename=test_{size}{unit}.bin",
        "Content-Type": "application/octet-stream"
    }

    return Response(generate_file(size_bytes), headers=headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)