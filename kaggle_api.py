import kagglehub


def get_kaggle_dir():

    # Download da versão atualizada da planilha
    path = kagglehub.dataset_download("italoxesteres/banks-complaints-and-customer-numbers-in-brazil")

    if (path):
        print("Dados baixados no path: ", path)

    return path