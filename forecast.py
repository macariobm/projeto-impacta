import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA


def forecast_complaints(full_df, steps=12):

    # Transforma o datetime em datetime
    full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])
    
    # Usa os dados mensais e soma as reclamacoes
    time_series = full_df.set_index('timestamp').resample('M')['quantidade de reclamações reguladas procedentes'].sum()
    
    # Configura o modelo ARIMA
    model = ARIMA(time_series, order=(1, 1, 1))
    model_fit = model.fit()
    
    # Gera o forecast
    forecast = model_fit.forecast(steps=steps)
    
    # Configura os resultados
    plt.figure(figsize=(10, 6))
    time_series.plot(label='Actual', legend=True)
    forecast.plot(label='Forecast', linestyle='--', legend=True)
    plt.title('Complaint Forecasting')
    plt.xlabel('Time')
    plt.ylabel('Number of Complaints')
    plt.grid(True)
    plt.show()
    

    # Retorna o forecast como DataFrame
    forecast_df = forecast.reset_index()
    forecast_df.columns = ['timestamp', 'predicted_complaints']

    # Converte datetime
    forecast_df['timestamp'] = forecast_df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return forecast_df
