import sqlite3
import yfinance as yf
import os
from datetime import datetime

def list_databases():
    db_files = [f for f in os.listdir() if f.endswith('.db')]  # data list
    
    if db_files:
        for db in db_files:
            print(f"- {db}")
    else:
        print("Error. There are non datebases in folder")

def update_data(ticker):
    """Data update."""
    try:
        db_name = f"{ticker}.db" 
        conn = sqlite3.connect(db_name)  
        # downlaod data
        data = yf.download(ticker, start="2013-01-01", end=datetime.today().strftime('%Y-%m-%d'), interval='1d')
        
        # save data
        data.to_sql(ticker, conn, if_exists='replace', index=True)
        
        print(f"Data for {ticker} succesfully updated {db_name}.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def main():
        
        print("Databeses: (.db)\n")
        list_databases() 
        update_data("VUSA.L")
        

if __name__ == "__main__":
    main() 
