import json
import spacy
import re

# Cargar el modelo de spaCy para el francés
nlp = spacy.load("fr_core_news_sm")

class FeatureEngineering:
    @staticmethod
    def load_data(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def normalize_field(data, fields_to_normalize):
        for item in data:
            for field in fields_to_normalize:
                # Normaliza campos directos
                if field in item and isinstance(item[field], str):
                    item[field] = re.sub(r'\s+', ' ', item[field].lower().strip())
                
                # Para campos anidados, como 'entreprise.nom'
                elif '.' in field:
                    subfields = field.split('.')
                    current_level = item
                    for i, subfield in enumerate(subfields):
                        if subfield in current_level:
                            if isinstance(current_level[subfield], str):
                                current_level[subfield] = re.sub(r'\s+', ' ', current_level[subfield].lower().strip())
                            elif i == len(subfields) - 1 and isinstance(current_level[subfield], list):
                                # Especial para listas de diccionarios, como 'competences'
                                for comp in current_level[subfield]:
                                    for key in comp:
                                        if isinstance(comp[key], str):
                                            comp[key] = re.sub(r'\s+', ' ', comp[key].lower().strip())
                            current_level = current_level.get(subfield, {})
                
                # Si el campo es una lista de diccionarios directamente en el nivel superior
                elif field in item and isinstance(item[field], list):
                    for comp in item[field]:
                        for key in comp:
                            if isinstance(comp[key], str):
                                comp[key] = re.sub(r'\s+', ' ', comp[key].lower().strip())

    @staticmethod
    def tokenize_and_lemmatize(data, text_fields):
        total_items = len(data)
        print_every = 100  # Ajusta este valor según la frecuencia con la que quieres ver el progreso

        for index, item in enumerate(data):
            if (index + 1) % print_every == 0:
                print(f"Procesando {index + 1} de {total_items} items...")

            for field in text_fields:
                # Comprueba si el campo existe en el diccionario y si es una cadena
                if field in item and isinstance(item[field], str):
                    doc = nlp(item[field])
                    # Extrae los lemas de los tokens y une los tokens en una cadena separada por espacios
                    item[field] = " ".join([token.lemma_ for token in doc])
                # Procesamiento para campos anidados, como 'entreprise.description'
                elif '.' in field:
                    subfields = field.split('.')
                    current_level = item
                    for i, subfield in enumerate(subfields[:-1]):
                        if subfield in current_level:
                            current_level = current_level[subfield]
                        else:
                            current_level = None
                            break
                    final_field = subfields[-1]
                    if current_level and final_field in current_level and isinstance(current_level[final_field], str):
                        doc = nlp(current_level[final_field])
                        current_level[final_field] = " ".join([token.lemma_ for token in doc])
        print("Tokenización y lematización completadas.")

    @staticmethod
    def save_clean_data(data, new_filepath):
        with open(new_filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def apply_feature_engineering(filepath):

        data = FeatureEngineering.load_data(filepath)
        FeatureEngineering.normalize_field(data, ['intitule', 'description', 'romeLibelle', 'appellationlibelle', 'entreprise.nom','entreprise.description', 'competences', 'qualificationLibelle', 'secteurActiviteLibelle', 'salaire.libelle'])
        FeatureEngineering.tokenize_and_lemmatize(data, ['description', 'entreprise.description'])

        new_filepath = filepath.replace('.json', '_fe.json')
        FeatureEngineering.save_clean_data(data, new_filepath)
