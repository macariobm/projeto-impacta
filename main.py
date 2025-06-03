from flask import Flask, jsonify, send_file
from data_processor import process_data, file_path
from forecast import forecast_complaints
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import io


app = Flask(__name__)

CORS(app)

# rota para visualização dos dados a serem fetched pelo matplotlib
@app.route('/dados', methods=['GET'])

def get_dados():
    data = process_data(file_path)
    return jsonify(data)

@app.route('/forecast-graph', methods=['GET'])

def forecast_plot():
    data = process_data(file_path)
    if not data:
        return jsonify({"Erro": "Não há dados"}), 400
    full_df = pd.DataFrame(data)
    forecasted_data = forecast_complaints(full_df)
    forecasted_json = forecasted_data.to_dict(orient='records')

    return jsonify({"Forecast:": forecasted_json}), 200

@app.route('/graph', methods=['GET'])
def plot_data():
    data = process_data(file_path)
    if not data:
        return jsonify({"Erro": "Não há dados"}), 400

    full_df = pd.DataFrame(data)

    # datetime
    full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])

    # reagrupa mensalmente
    time_series = full_df.set_index('timestamp').resample('M')['quantidade de reclamações reguladas procedentes'].sum()

    # mantém colunas e as renomeia
    df = df[['instituição financeira', 'quantidade de reclamações reguladas procedentes']]
    df = df.rename(columns={
        'instituição financeira': 'instituicao',
        'quantidade de reclamações reguladas procedentes': 'reclamacoes'
    })

    # pega as 10 primeiras no ranking
    df = df.sort_values(by='reclamacoes', ascending=False).head(10)

    # faz o plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['instituicao'], df['reclamacoes'], color='steelblue')
    ax.set_xlabel('Reclamações')
    ax.set_ylabel('Instituição')
    ax.set_title('Top 10 Instituições por Reclamações')
    plt.tight_layout()

    # salva o png
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)

    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)