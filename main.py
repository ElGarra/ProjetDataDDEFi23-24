from models.cleaner import DataCleaner
from models.feature_engineering import FeatureEngineering

if __name__ == "__main__":
    first_filepath = 'assets/offers.json'  
    DataCleaner.process_data(first_filepath)
    second_filepath = 'assets/offers_cleaned.json'  
    FeatureEngineering.apply_feature_engineering(second_filepath)
