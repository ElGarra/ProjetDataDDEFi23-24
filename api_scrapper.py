from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime, timedelta
import urllib.parse

class ApiScrapper:
    def __init__(self):
        load_dotenv()  # Cargar las variables de entorno del archivo .env
        self.client_id = str(os.getenv('CLIENT_ID'))
        self.client_secret = str(os.getenv('CLIENT_SECRET'))
        self.scope = str(os.getenv('SCOPE'))
        self.request_count = 0

    def generate_access_token(self):
        url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {"realm": '/partenaire'}
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }

        response = requests.post(url, headers=headers, data=payload, params=params)

        if response.status_code != 200:
            try:
                error_details = response.json()
                print(f"Error details: {error_details}")
            except ValueError:
                print(f"Error: {response.status_code}, Response: {response.text}")
            return None
        return response.json()

    def extract_data(self, access_token, start, end):
        iso_start = urllib.parse.quote(start.isoformat(timespec='seconds') + "Z")
        iso_end = urllib.parse.quote(end.isoformat(timespec='seconds') + "Z")
        reqUrl = f"https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?minCreationDate={iso_start}&maxCreationDate={iso_end}"

        headersList = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.request("GET", reqUrl, headers=headersList)

        self.request_count += 1
        print(f"> Request N° {self.request_count}")
        print(f"Status: {response.status_code}")

        if response.status_code in [200, 206]:
            return response.json()['resultats']
        else:
            try:
                error_details = response.json()
                print(f"Error details: {error_details}")
            except ValueError:
                print(f"Error: {response.status_code}, Response: {response.text}")
            return None

    def collect_all_offers(self):
        all_offers = []
        start = datetime(2023, 12, 6)
        end = datetime(2023, 12, 7)
        total_requests = 0

        with open('offers_log.txt', 'w', encoding='utf-8') as log_file:
            while total_requests < 33:
                print(f"Extracting offers from {start} to {end}")
                token_info = self.generate_access_token()
                if token_info and 'access_token' in token_info:
                    access_token = token_info['access_token']
                    offers = self.extract_data(access_token, start, end)
                    
                    if offers is not None:
                        log_file.write(f"{start.date()} to {end.date()}: {len(offers)} offers found\n")
                        print(f"{len(offers)} offers found...")
                        all_offers.extend(offers)

                    # Incrementa las fechas independientemente de si hay ofertas o no
                    start += timedelta(days=1)
                    end += timedelta(days=1)
                else:
                    print("Error obtaining access token")
                    break

                total_requests += 1

        # Guardar todas las ofertas en un archivo JSON
        file_name = 'all_offers.json'
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                existing_offers = json.load(file)
            all_offers.extend(existing_offers)

        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(all_offers, file, ensure_ascii=False, indent=4)

        print(len(all_offers))

        return all_offers
    
# Uso
scrapper = ApiScrapper()
all_offers = scrapper.collect_all_offers()

