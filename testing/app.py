import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime

# Wybierz ticker
ticker = "VUSA.L"

# Pobierz dane historyczne
data = yf.download(ticker, start="2013-01-01", end=datetime.today().strftime('%Y-%m-%d'), interval='1d')

# Ustanowienie połączenia z bazą danych SQLite (lub utworzenie nowej bazy danych)
conn = sqlite3.connect('Vanguard.db')

# Zapisz dane do tabeli w bazie danych
data.to_sql(ticker, conn, if_exists='replace', index=True)

# Zamykanie połączenia
conn.close()

print("Dane zostały zapisane do bazy danych.")
