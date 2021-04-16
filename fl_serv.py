from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/test')
def test():
    return "qwe"


@app.route('/')
def hello_world():
    return jsonify({'code': 200})


if __name__ == '__main__':
    app.run()
