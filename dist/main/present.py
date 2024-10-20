import pickle
import pandas as pd
import numpy as np
from hmmlearn import hmm
import sqlite3
import matplotlib
matplotlib.use('TkAgg')  # Użyj backendu TkAgg
import matplotlib.pyplot as plt

# Funkcja do wczytywania modelu HMM z pliku
def load_model(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model


# Funkcja do pobierania ostatnich danych z bazy danych SQLite
def get_recent_data(ticker, num_days):
    db_name = 'VUSA.L.db'  # Nazwa pliku bazy danych
    conn = sqlite3.connect(db_name)
    
    query = f"SELECT * FROM '{ticker}' ORDER BY Date DESC LIMIT {num_days}"
    print(f"Executing query: {query}")  # Wydrukuj zapytanie
    data = pd.read_sql_query(query, conn)  # Wczytanie danych

    conn.close()  # Zamknij połączenie z bazą danych
    return data

# Funkcja do obliczania zwrotów
def calculate_returns(data):
    # Można obliczyć zwroty na podstawie zamknięcia oraz innych kolumn
    data['Returns_Close'] = data['Close'].pct_change()
    data['Returns_Open'] = data['Open'].pct_change()
    data['Returns_High'] = data['High'].pct_change()
    data['Returns_Low'] = data['Low'].pct_change()
    return data.dropna()


def get_background_color(state):
    """Zwraca kolor tła w zależności od ukrytego stanu."""
    if state == 1:
        return "\033[48;5;46m"  # Zielony
    elif state == 2:
        return "\033[48;5;22m"  # Ciemnozielony
    elif state == 3:
        return "\033[48;5;226m"  # Żółty
    elif state == 4:
        return "\033[48;5;214m"  # Pomarańczowy
    elif state == 5:
        return "\033[48;5;196m"  # Czerwony
    elif state == 6:
        return "\033[48;5;124m"  # Ciemnoczerwony
    elif state == 7:
        return "\033[48;5;88m"   # Ciemnoczerwony 2
    elif state == 8:
        return "\033[48;5;16m"   # Czarny
    else:
        return "\033[0m"          # Domyślny

def display_hidden_states(recent_data, hidden_states):
    # Upewnij się, że hidden_states i recent_data mają tę samą długość
    if len(recent_data) != len(hidden_states):
        print("Błąd: Długość hidden_states i recent_data musi być taka sama.")
        return
    
    # Utwórz nową ramkę danych do wyświetlenia
    output_data = recent_data[['Date', 'Close']].copy()
    output_data['Hidden State'] = hidden_states  # Dodaj kolumnę z ukrytymi stanami

    # Wyświetl dane w formacie tabelarycznym z kolorami
    for index, row in output_data.iterrows():
        bg_color = get_background_color(row['Hidden State'])
        print(f"{bg_color} {row['Date']} | {row['Close']} | Hidden State: {row['Hidden State']} \033[0m")
def predict_hidden_states(data, model):
    # Przygotuj dane wejściowe do modelu, np. z normalizacją lub standaryzacją
    features = data[['Open', 'High', 'Low', 'Close', 'Volume', 'Returns_Close', 'Returns_Open', 'Returns_High', 'Returns_Low']]
    
    # Upewnij się, że model dostaje dane w odpowiednim formacie
    hidden_states = model.predict(features)  # Przykład, dostosuj zgodnie z metodą przewidywania
    return hidden_states

def predict_hidden_states_and_probs(data, model):
    # Przygotuj dane wejściowe do modelu
    features = data[['Returns_Close']].values.reshape(-1, 1)
    
    # Przewidywanie stanu i prawdopodobieństw
    hidden_states = model.predict(features)
    probabilities = model.predict_proba(features)
    
    return hidden_states, probabilities

def display_hidden_states_with_probs(recent_data, hidden_states, probabilities):
    if len(recent_data) != len(hidden_states):
        print("Błąd: Długość hidden_states i recent_data musi być taka sama.")
        return
    
    output_data = recent_data[['Date', 'Close']].copy()
    output_data['Hidden State'] = hidden_states  # Dodaj kolumnę z ukrytymi stanami
    
    # Dodaj kolumnę z prawdopodobieństwami dla stanu ukrytego
    output_data['Probabilities'] = [prob[hidden_states[i]] for i, prob in enumerate(probabilities)]
    
    # Wyświetl dane w formacie tabelarycznym z kolorami, odwrócona kolejność
    for index, row in output_data.iloc[::-1].iterrows():  # Odwróć kolejność wierszy
        bg_color = get_background_color(row['Hidden State'])
        print(f"{bg_color} {row['Date']} | {row['Close']} | Hidden State: {row['Hidden State']} | Probability: {row['Probabilities']:.4f} \033[0m")


# Główna funkcja
def main():
    # Wczytaj model z pliku
    model = load_model('VUSA_model.pkl')
    
    # Pobierz dane z ostatnich dni (np. 30 dni)
    ticker = "VUSA.L"
    recent_data = get_recent_data(ticker, 90)
    
    # Oblicz zwroty
    recent_data = calculate_returns(recent_data)

    # Przygotuj dane do predykcji (np. użyj ostatnich zwrotów)
    features = recent_data[['Returns_Close']].values.reshape(-1, 1)
    #print(recent_data)
    
    # Przewidywanie stanu
    hidden_states = model.predict(features)

    # Przewidywanie stanu i prawdopodobieństw
    hidden_states, probabilities = predict_hidden_states_and_probs(recent_data, model)
    
    # Wyświetlenie stanu i prawdopodobieństw
    display_hidden_states_with_probs(recent_data, hidden_states, probabilities)
    print("average hidden state; scale 0-7; 90 days period")
    print('%.3f' % (sum(hidden_states) / 90))

    if (sum(hidden_states) / 90) < 4:
        print("\033[48;5;46m average HOSSA state \033[0m")

    else:
       print("\033[48;5;196m average BESSA state \033[0m")

   
if __name__ == "__main__":
    main()
