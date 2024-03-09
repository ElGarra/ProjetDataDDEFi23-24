import json
from collections import defaultdict

class DataCleaner:

    @staticmethod
    def load_data(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def remove_duplicates(data):
        unique_data = {}
        duplicates = []

        for each in data:
            if each['id'] in unique_data:
                duplicates.append(each)
            else:
                # Add the first aparition of each offer
                unique_data[each['id']] = each

        if duplicates:
            with open('duplicates.txt', 'w', encoding='utf-8') as file:
                for duplicate in duplicates:
                    file.write(json.dumps(f"Offer {duplicate['id']} duplicated", ensure_ascii=False) + '\n')

        # return the list without duplicates
        return list(unique_data.values())

    @staticmethod
    def calculate_field_percentage(data):
        field_count = defaultdict(int)
        total_entries = len(data)

        def count_fields(entry, prefix=''):
            if isinstance(entry, dict):
                for key, value in entry.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    if isinstance(value, dict):
                        count_fields(value, full_key)
                    elif isinstance(value, list):
                        # Verify if the list contains dicts and count just once
                        if value and isinstance(value[0], dict):
                            # Count each field of the dict inside the list juste once
                            unique_fields = set()
                            for item in value:
                                for subkey in item.keys():
                                    unique_fields.add(f"{full_key}.{subkey}")
                            for unique_field in unique_fields:
                                field_count[unique_field] += 1
                        else:
                            # If the list doesn't contains dicts, so count the complete list as a field
                            field_count[full_key] += 1
                    else:
                        field_count[full_key] += 1

        for item in data:
            count_fields(item)

        field_percentage = {field: (count / total_entries) * 100 for field, count in field_count.items()}
        return field_percentage

    @staticmethod
    def generate_field_percentage_report(field_percentage):
        report = "Field Appearance Percentage Report\n=================================\n\n"
        for field, percentage in field_percentage.items():
            report += f"{field}: {percentage:.2f}%\n"
        return report

    @staticmethod
    def _delete_field_recursive(dict_, fields):
        if len(fields) > 1 and fields[0] in dict_:
            if isinstance(dict_[fields[0]], dict):
                DataCleaner._delete_field_recursive(dict_[fields[0]], fields[1:])
            elif isinstance(dict_[fields[0]], list):
                for item in dict_[fields[0]]:
                    if isinstance(item, dict):
                        DataCleaner._delete_field_recursive(item, fields[1:])
        elif fields[0] in dict_:
            del dict_[fields[0]]

    @staticmethod
    def filter_fields_by_percentage(data, field_percentage, threshold=32):
        fields_to_delete = [field for field, percentage in field_percentage.items() if percentage < threshold]

        for dict_ in data:
            for field in fields_to_delete:
                split_field = field.split('.')
                DataCleaner._delete_field_recursive(dict_, split_field)
                
        return data

    @staticmethod
    def delete_field_from_data(data, field_to_delete):
        def delete_field(dict_, fields):
            if "." in fields:  # Verify if it's an anidated field
                current_field, rest_of_fields = fields.split(".", 1)
                if current_field in dict_:
                    if isinstance(dict_[current_field], dict):
                        delete_field(dict_[current_field], rest_of_fields)
                    elif isinstance(dict_[current_field], list):
                        for item in dict_[current_field]:
                            if isinstance(item, dict):
                                delete_field(item, rest_of_fields)
            else:
                if fields in dict_:
                    del dict_[fields]

        fields_split = field_to_delete.split(".")
        for dict_ in data:
            delete_field(dict_, field_to_delete)

        return data
    
    @staticmethod
    def remove_empty_or_trivial_lists(data):
        fields_removed = []  # List to store the name of the deleted fields
        for dict_ in data:
            keys_to_delete = [key for key, value in dict_.items() if isinstance(value, list) and (not value or all(isinstance(item, dict) and not item for item in value))]
            fields_removed.extend(keys_to_delete)  # Add the name of the fields to the list
            for key in keys_to_delete:
                del dict_[key]  # Delete the field of the dictionary
        return list(set(fields_removed))  # Return a list of deleted fields

    @staticmethod
    def save_clean_data(data, new_filepath):
        with open(new_filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def print_unique_fields(data):
        # Print all the fields after cleaning the data
        unique_fields = set()
        for dict_ in data:
            for field in dict_:
                unique_fields.add(field)
        
        unique_fields_list = sorted(list(unique_fields))  # Convert to a list and order
        print("Unique fields of the data:", unique_fields_list)
        return unique_fields_list

    @staticmethod
    def process_data(filepath):
        data = DataCleaner.load_data(filepath)
        report_lines = []  # List to store the lines of the "deleted fields" report

        unique_data = DataCleaner.remove_duplicates(data)

        field_percentage = DataCleaner.calculate_field_percentage(unique_data)
        initial_report = DataCleaner.generate_field_percentage_report(field_percentage)
        # Store the initial report of fields %
        with open(filepath.replace('.json', '_initial_percentage_report.txt'), 'w', encoding='utf-8') as file:
            file.write(initial_report)

        filtered_data = DataCleaner.filter_fields_by_percentage(unique_data, field_percentage, 32)
        fields_removed_by_percentage = [key for key, value in field_percentage.items() if value < 32]

        non_desired_fields = [
            'origineOffre', 
            'dateCreation', 
            'dateActualisation', 
            'contact', 
            'nombrePostes', 
            'accessibleTH', 
            'offresManqueCandidats', 
            'dureeTravailLibelle', 
            'dureeTravailLibelleConverti', 
            'typeContrat', 
            'typeContratLibelle', 
            'natureContrat', 
            'lieuTravail', 
            'alternance'
        ]

        # Delete fields manually by criteria
        for field in non_desired_fields:
            DataCleaner.delete_field_from_data(filtered_data, field)

        empty_or_trivial_fields_removed = DataCleaner.remove_empty_or_trivial_lists(filtered_data)
        
        # Generation of the "deleted fields" report
        report_lines.append("Deleted fields by percentage of apparition:")
        report_lines.extend(fields_removed_by_percentage)
        report_lines.append("\nDeleted fields by criteria:")
        report_lines.extend(non_desired_fields)
        report_lines.append("\nFields with empty lists of trivial dicts:")
        report_lines.extend(empty_or_trivial_fields_removed)

        final_report_path = filepath.replace('.json', '_fields_removal_report.txt')
        with open(final_report_path, 'w', encoding='utf-8') as final_report_file:
            final_report_file.write("\n".join(report_lines))

        new_field_percentage = DataCleaner.calculate_field_percentage(filtered_data)
        final_percentage_report = DataCleaner.generate_field_percentage_report(new_field_percentage)
        with open(filepath.replace('.json', '_final_percentage_report.txt'), 'w', encoding='utf-8') as file:
            file.write(final_percentage_report)

        DataCleaner.print_unique_fields(filtered_data)
        
        # Store the clean data
        new_filepath = filepath.replace('.json', '_cleaned.json')
        DataCleaner.save_clean_data(filtered_data, new_filepath)

        return data
