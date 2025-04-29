from flask import Flask, jsonify
from data_processor import process_data, file_path
from forecast import forecast_complaints
from flask_cors import CORS
import pandas as pd
import plotly.express as px


app = Flask(__name__)

CORS(app)

# rota para visualização dos dados a serem fetched pelo Grafana
@app.route('/dados', methods=['GET'])

def get_dados():
    data = process_data(file_path)
    return jsonify(data)

@app.route('/forecast', methods=['GET'])

def forecast_data():
    data = process_data(file_path)
    if not data:
        return jsonify({"Erro": "Não há dados"}), 400
    full_df = pd.DataFrame(data)
    forecasted_data = forecast_complaints(full_df)
    forecasted_json = forecasted_data.to_dict(orient='records')

    return jsonify({"Forecast:": forecasted_json}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)