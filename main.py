from toolkit.cleaner import CSV_Cleaner
from toolkit.validator import CSV_Validator
import json

if __name__ == "__main__":
    with open('examples/rules_messy.json', 'r') as f:
        rules = json.loads(f.read())
        
    cleaner = CSV_Cleaner(rules, 'examples/messy_csv_file.csv')
    
    cleaner.load_data()
    cleaner.clean_data()
    cleaner.save_data('examples/cleaned_csv_file.csv')
    
    print(cleaner.data_to_string)
    
    validator = CSV_Validator(rules, 'examples/validation_log.txt', data=cleaner.pandas)
