from flask import Flask, jsonify
from data_processor import process_data, file_path
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

# rota para visualização dos dados a serem fetched pelo Grafana
@app.route('/dados', methods=['GET'])

def get_dados():
    data = process_data(file_path)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)