import os
# from dotenv import load_dotenv
import requests
import json
import time

class ApiScrapper:
    def __init__(self):
        # load_dotenv()  # Load the environment variables from .env file
        # self.client_id = os.getenv('CLIENT_ID')
        # self.client_secret = os.getenv('CLIENT_SECRET')
        # self.scope = os.getenv('SCOPE')
        # print(self.client_id, "\n", self.client_secret, "\n", self.scope)
        self.client_id = "PAR_projetdata2324_771b276340f58eae3c483747cf0ab4104e76ac354855b57ae2e22bd07495b4dd"
        self.client_secret = "18c07536cce9ea0d94216fca2181efa18561c599119af21a115a2073d10089fe"
        self.scope = "api_offresdemploiv2 application_PAR_projetdata2324_771b276340f58eae3c483747cf0ab4104e76ac354855b57ae2e22bd07495b4dd o2dsoffre"
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
            print(f"Error: {response.status_code}, Response: {response.text}")
            return None
        return response.json()

    def extract_data(self, access_token, start, end):
        url = 'https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search'
        headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
        params = {"range": f'{start}-{end}'}

        response = requests.get(url, headers=headers, params=params)

        self.request_count += 1
        print(f"> Request N° {self.request_count}")
        print(f"Status: {response.status_code}")

        if response.status_code == 206:
            return response.json()['resultats']
        else:
            return f"Error: {response.status_code}"
        
    def collect_all_offers(self):
        all_offers = []
        start = 0
        end = 149
        total_requests = 0

        while total_requests < 30:

            # if total_requests % 20 == 0 and total_requests != 0:
            #     print("Pausing for 1 minute to avoid rate limits...")
            #     time.sleep(60)  # Pause for 1 minute


            token_info = self.generate_access_token()
            time.sleep(5)
            if 'access_token' in token_info:
                access_token = token_info['access_token']
                offers = self.extract_data(access_token, start, end)
                
                if isinstance(offers, list):
                    all_offers.extend(offers)
                    start += 150
                    end += 150
                else:
                    print("Error in request:", offers)
                    break
            else:
                print("Error obtaining access token")
                break

            total_requests += 1

        # Check if the file exists
        file_name = 'all_offers.json'
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                existing_offers = json.load(file)
            all_offers.extend(existing_offers)

        # Save all offers to a JSON file
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(all_offers, file, ensure_ascii=False, indent=4)

        print(len(all_offers))

        return all_offers

# Usage
scrapper = ApiScrapper()
all_offers = scrapper.collect_all_offers()
