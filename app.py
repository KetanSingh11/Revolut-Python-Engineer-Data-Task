from flask import Flask
from flask import request, jsonify
import nest


app = Flask(__name__)

@app.route('/test', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/', methods=['POST'])
def nest_service():
    if request.method == 'POST':
        return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)