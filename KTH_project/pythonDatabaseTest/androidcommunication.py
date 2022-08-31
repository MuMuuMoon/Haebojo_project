from flask import Flask, make_response, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if (request.method == 'POST'):
        value = request.get_data()

        print(value)
    print("123")
    return "Flask Server & Android are Working Successfully"


if __name__ == '__main__':
    app.run('0.0.0.0', 5555)