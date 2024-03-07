from models.cleaner import DataCleaner

if __name__ == "__main__":
    filepath = 'assets/offers.json'  # Ajusta la ruta al archivo
    DataCleaner.process_data(filepath)
