import subprocess

def main():
    # Wywołanie innego skryptu
    subprocess.run(["python", "data_check.py"])
    subprocess.run(["python", "present.py"])
    # Czekaj na input użytkownika przed zakończeniem
    input("Naciśnij Enter, aby zakończyć...")

if __name__ == "__main__":
    main()
