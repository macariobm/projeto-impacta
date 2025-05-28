import os
import datetime
import pandas as pd
from kaggle_api import get_kaggle_dir

dir_path = get_kaggle_dir()
file = 'Reclamacoes e clientes - Bacen.xlsx'
file_path = os.path.join(dir_path, file)

def process_data(file_path):
    if os.path.exists(file_path):

        all_data = []

        # Lê as planilhas
        planilhas = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        for planilha, df in planilhas.items():
            print(f"Lendo a planilha: {planilha}")
            df.columns = df.columns.str.strip().str.lower()

            colunaPadrao = 'quantidade de reclamações reguladas procedentes'
            colunaAlternativa = 'quantidade de reclamaçoes procedentes'

            # Valida as colunas
            if colunaPadrao not in df.columns:
                if colunaAlternativa in df.columns:
                    df.rename(columns={colunaAlternativa: colunaPadrao}, inplace=True)
                    print(f"A coluna '{colunaAlternativa}' foi renomeada para '{colunaPadrao}' na planilha '{planilha}'")
                else:
                    print(f"Faltam colunas obrigatórias na planilha '{planilha}'")
                    continue

            # Preenche valores vazios
            df.fillna('Sem valores', inplace=True)

            # Faz um 'append' de todos os dados
            all_data.append(df)

        if not all_data:
            print("Sem dados válidos nas planilhas")
            return []

        # Concatena os dados em um DataFrame
        full_df = pd.concat(all_data, ignore_index=True)
        print("DataFrame após concatenação:")
        print(full_df.head())

        # Adiciona tiemstamp
        full_df['timestamp'] = datetime.datetime.now().isoformat()

        # Verifica as colunas obrigatórias
        required_columns = ['timestamp', 'instituição financeira', 'quantidade de reclamações reguladas procedentes']
        missing_columns = [col for col in required_columns if col not in full_df.columns]
        if missing_columns:
            print(f"Faltam as seguintes colunas obrigatórias: {missing_columns}.")
            return []

        # Agrupa os dados por instituição financeira e os agrega
        grouped_df = full_df.groupby('instituição financeira', as_index=False).agg({
            'quantidade de reclamações reguladas procedentes': 'sum',
            'timestamp': 'first'
        })

        print("DataFrame agrupado:")
        print(grouped_df)

        # Converte para JSON
        result = grouped_df.to_dict(orient='records')
        print("Dados agrupados finais:")
        print(result)

        return result

    else:
        print(f"O arquivo '{file}' não existe no path '{dir_path}'")
        return []

# Executa a função
cleaned_data = process_data(file_path)