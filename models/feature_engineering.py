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
        pass
        # Aquí iría la implementación de tokenize_and_lemmatize tal como se detalló anteriormente.

    @staticmethod
    def save_clean_data(data, new_filepath):
        with open(new_filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def apply_feature_engineering(filepath):
        """
        Applies text normalization and tokenization-lemmatization to specified fields in the dataset.
        
        Parameters:
        - data (list): List of dictionaries representing the dataset.
        - fields_to_process (list): List of fields to be processed.
        """

        data = FeatureEngineering.load_data(filepath)
        FeatureEngineering.normalize_field(data, ['intitule', 'description', 'romeLibelle', 'appellationlibelle', 'entreprise.nom','entreprise.description', 'competences', 'qualificationLibelle', 'secteurActiviteLibelle', 'salaire.libelle'])
        # FeatureEngineering.tokenize_and_lemmatize(data, fields_to_process)

        new_filepath = filepath.replace('.json', '_fe.json')
        FeatureEngineering.save_clean_data(data, new_filepath)
