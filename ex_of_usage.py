from toolkit.cleaner import CSV_Cleaner
from toolkit.validator import CSV_Validator, NumericValidationError
from toolkit.report_generator import Report
import json

if __name__ == "__main__":
    with open('examples/rules_messy.json', 'r') as f:
        rules = json.loads(f.read())
        
    cleaner = CSV_Cleaner(rules, 'examples/messy_csv_file.csv')
    
    cleaner.load_data()
    cleaner.clean_data()
    cleaner.save_data('examples/cleaned_csv_file.csv')
    
    print(cleaner.data_to_string)
    cleaner.pandas.info()
    
    validator = CSV_Validator(rules, 'examples/validation_log.txt', data=cleaner.pandas)
    try:
        validator.validate_data()
    except NumericValidationError:
        print("Numeric validation errors found. See log for details.")
    
    Report(cleaner.pandas, 
           title="Cleaned CSV Report").generate(include_statistics=True, 
                                                clean_data=True,
                                                validation_log='examples/validation_log.txt', 
                                                output_path='examples/report.txt')