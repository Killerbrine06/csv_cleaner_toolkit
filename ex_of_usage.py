from toolkit.cleaner import CSVCleaner
from toolkit.validator import CSVValidator
from toolkit.report_generator import Report
import json

if __name__ == "__main__":
    with open('examples/rules_messy.json', 'r') as f:
        rules = json.loads(f.read())
        
    cleaner = CSVCleaner(rules, 'examples/messy_csv_file.csv')
    
    cleaner.load_data()
    cleaner.clean_data()
    cleaner.save_data('examples/cleaned_csv_file.csv')
    
    cleaner.pandas.info()
    
    validator = CSVValidator(rules, data=cleaner.pandas)
    log = validator.validate_data()
    
    Report(cleaner.pandas, 
           title="Cleaned CSV Report").generate(include_statistics=True, 
                                                clean_data=True, validation_log=log,
                                                output_path='examples/report.txt')