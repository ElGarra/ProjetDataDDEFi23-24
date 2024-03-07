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
                unique_data[each['id']] = each

        if duplicates:
            with open('duplicates.txt', 'w', encoding='utf-8') as file:
                for duplicate in duplicates:
                    file.write(json.dumps(f"Offer {duplicate['id']} duplicated", ensure_ascii=False) + '\n')

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
                        # Verificar si la lista contiene diccionarios y contar solo una vez
                        if value and isinstance(value[0], dict):
                            # Contar cada campo en el diccionario dentro de la lista solo una vez
                            unique_fields = set()
                            for item in value:
                                for subkey in item.keys():
                                    unique_fields.add(f"{full_key}.{subkey}")
                            for unique_field in unique_fields:
                                field_count[unique_field] += 1
                        else:
                            # Si la lista no contiene diccionarios, contar la lista entera como un campo
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
    def filter_fields_by_percentage(data, field_percentage, threshold=33):
        fields_to_delete = [field for field, percentage in field_percentage.items() if percentage < threshold]

        for dict_ in data:
            for field in fields_to_delete:
                split_field = field.split('.')
                DataCleaner._delete_field_recursive(dict_, split_field)
                
        return data

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
    def delete_field_from_data(data, field_to_delete):
        def delete_field(dict_, fields):
            if "." in fields:  # Verificar si el campo es anidado
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
    def save_clean_data(data, new_filepath):
        with open(new_filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def process_data(filepath):
        # Carga los datos
        data = DataCleaner.load_data(filepath)

        # Elimina duplicados
        unique_data = DataCleaner.remove_duplicates(data)

        # Calcula el porcentaje de aparición de cada campo
        field_percentage = DataCleaner.calculate_field_percentage(unique_data)
        initial_report = DataCleaner.generate_field_percentage_report(field_percentage)
        with open(filepath.replace('.json', '_initial_percentage_report.txt'), 'w', encoding='utf-8') as file:
            file.write(initial_report)

        # Filtra campos por porcentaje de aparición
        filtered_data = DataCleaner.filter_fields_by_percentage(unique_data, field_percentage, 32)

        # Elimina cualquier campo específico no deseado
        DataCleaner.delete_field_from_data(filtered_data, 'origineOffre')

        # Calcula de nuevo el porcentaje de aparición de cada campo después de la limpieza adicional
        new_field_percentage = DataCleaner.calculate_field_percentage(filtered_data)
        final_report = DataCleaner.generate_field_percentage_report(new_field_percentage)
        with open(filepath.replace('.json', '_final_percentage_report.txt'), 'w', encoding='utf-8') as file:
            file.write(final_report)

        # Guarda los datos limpios y procesados
        new_filepath = filepath.replace('.json', '_cleaned.json')
        DataCleaner.save_clean_data(filtered_data, new_filepath)
        return data



