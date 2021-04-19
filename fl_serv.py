from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder="admin")


@app.route('/test')
def test():
    return jsonify({'code': 200})


@app.route('/')
def hello_world():
    # return app.send_static_file('/index.html')
    return send_from_directory('admin', 'index.html')


@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('admin', 'index.html')


if __name__ == '__main__':
    app.run()
