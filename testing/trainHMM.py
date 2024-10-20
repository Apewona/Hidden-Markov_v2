import numpy as np
import pandas as pd
from hmmlearn import hmm
import sqlite3
import pickle
# Funkcja do wczytywania danych z bazy danych
def load_data(ticker):
    db_name = f"{ticker}.db"  # Nazwa pliku bazy danych
    conn = sqlite3.connect(db_name)
    
    query = f"SELECT * FROM '{ticker}'"
    print(f"Executing query: {query}")  # Wydrukuj zapytanie
    data = pd.read_sql_query(query, conn)  # Wczytanie wszystkich danych
    conn.close()
    return data

# Funkcja do obliczania zwrotów
def calculate_returns(data):
    # Obliczanie zwrotów dla zamknięcia oraz innych cech
    data['Returns_Close'] = data['Close'].pct_change()
    data['Returns_Open'] = data['Open'].pct_change()
    data['Returns_High'] = data['High'].pct_change()
    data['Returns_Low'] = data['Low'].pct_change()
    return data.dropna()  # Usunięcie NaN

def list_tables(conn):
    """Wyświetla wszystkie tabele w bazie danych."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    cursor.close()
    return tables

# Funkcja do trenowania modelu HMM
def train_hmm(data):
    # Ustawienie modelu HMM z włączonym trybem wyświetlania postępu
    model = hmm.GaussianHMM(n_components=8, covariance_type="diag", n_iter=1000, verbose=True)  
    model.fit(data)  # Trenowanie modelu na danych
    return model

def main():
    data = load_data("VUSA.L")  # Wczytanie danych z bazy danych
    data = calculate_returns(data)  # Obliczenie zwrotów

    # Użyj wszystkich zwrotów jako cech
    features = data[['Returns_Close', 'Returns_Open', 'Returns_High', 'Returns_Low']].values.reshape(-1, 4)

    # Wytrenuj model HMM na zwrotach
    model = train_hmm(features)

    print("Model HMM został pomyślnie wytrenowany. model:")
    print("Macierz przejścia:")
    print(model.transmat_)

    # Zapisz model do pliku
    with open('VUSA_model.pkl', 'wb') as file:
        pickle.dump(model, file)
if __name__ == "__main__":
    main()
