from flask import Flask, request
from flask.logging import default_handler, Formatter as LoggingFormatter
from function import get, put, post, delete, patch, search
from uuid import uuid4
import os


class RequestFormatter(LoggingFormatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        record.request_id = request.headers.get(os.getenv('REQUEST_ID_HEADER_NAME', 'X-Correlation-Id'), str(uuid4())) or str(uuid4())
        return super().format(record)


app = Flask(__name__)
formatter = RequestFormatter('[%(asctime)s] %(remote_addr)s - %(request_id)s - %(url)s - %(levelname)s - %(module)s: %(message)s')
default_handler.setFormatter(formatter)


@app.route("/<object_id>", methods=["GET"])
def handle_get(object_id):
    return get(request, object_id)

@app.route("/<object_id>", methods=["PUT"])
def handle_put(object_id):
    return put(request, object_id)


@app.route("/<object_id>", methods=["DELETE"])
def handle_delete(object_id):
    return delete(request, object_id)


@app.route("/<object_id>", methods=["PATCH"])
def handle_patch(object_id):
    return patch(request, object_id)


@app.route("/<object_id>", methods=["POST"])
def post(object_id):
    return update(request, object_id)



@app.route("/", methods=["POST"])
def post():
    return post(request)


@app.route("/", methods=["GET"])
def handle_search():
    return search(request)

if __name__ == '__main__':
    if os.getenv('SERVER', 'gevent'):
        from gevent.pywsgi import WSGIServer
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    else:
        app.run(host='0.0.0.0', port=5000, debug=False)
