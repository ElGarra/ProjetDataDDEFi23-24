import json
from collections import defaultdict

class DataCleaner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def remove_duplicates(self):
        unique_data = {}
        duplicates = []

        for each in self.data:
            if each['id'] in unique_data:
                duplicates.append(each)
            else:
                unique_data[each['id']] = each

        if duplicates:
            with open('../assets/duplicates.txt', 'w', encoding='utf-8') as file:
                for duplicate in duplicates:
                    file.write(json.dumps(f"Offer {duplicate['id']} duplicated and removed from the json", ensure_ascii=False) + '\n')

        self.data = list(unique_data.values())

    def save_clean_data(self, new_filepath):
        with open(new_filepath, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def field_percentage_report(self):
        field_count = defaultdict(int)
        total_entries = len(self.data)
        self.missing_data = []

        def count_fields(entry, prefix='', list_count=1):
            for key, value in entry.items():
                full_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, list) and value and isinstance(value[0], dict):
                    for item in value:
                        count_fields(item, full_key, len(value))
                else:
                    field_count[full_key] += 1 / list_count

        for item in self.data:
            count_fields(item)

        with open('../assets/field_percentage_report.txt', 'w', encoding='utf-8') as file:
            file.write("Field Appearance Percentage Report\n")
            file.write("=================================\n\n")
            for field, count in field_count.items():
                percentage = (count / total_entries) * 100
                file.write(f"{field}: {percentage:.2f}%\n")
                if ( count / total_entries ) < 0.35:
                    self.missing_data.append(field)
                    # print(f"{field}: {percentage:.2f}%\n")
        
    def delete_missing_data(self, new_filepath):
        with open(new_filepath, 'r', encoding='utf-8') as file:
            self.non_duplicate_data = json.load(file)
        print(self.non_duplicate_data[0])


# Uso de la clase
cleaner = DataCleaner('../assets/offers.json')
# cleaner.remove_duplicates()
# cleaner.save_clean_data('../assets/non_duplicates_offers.json')
# cleaner.field_percentage_report()
cleaner.delete_missing_data('../assets/non_duplicates_offers.json')


