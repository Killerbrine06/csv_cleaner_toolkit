from toolkit.cleaner import CSV_Cleaner
from toolkit.validator import CSV_Validator
from toolkit.report_generator import Report
import json, argparse, os, sys, logging
import pandas as pd

class InvalidPathError(Exception):
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Clean and validate a CSV file based on provided rules.')
    parser.add_argument('csv_path', type=str, help='Path to the CSV file to be cleaned and validated.')
    parser.add_argument('rules_path', type=str, help='Path to the JSON file containing cleaning and validation rules.')
    parser.add_argument('-o', '--output_path', type=str, required=True, help='Path to save the cleaned file.')
    parser.add_argument('-r', '--report', action='store_true', help='Generate a report after cleaning and validation.')
    parser.add_argument('--verbose', type=int, choices=[0, 1, 2], default=1, help='Set the verbosity level: 0 = no output, 1 = prints out information about the cleaned file, 2 = 1 and validation log.')

    args = parser.parse_args()
    return args

def validate_paths(args: argparse.Namespace):
    if not os.path.exists(args.csv_path):
        raise InvalidPathError(f"Error: CSV file '{args.csv_path}' does not exist.")

    if not os.path.exists(args.rules_path):
        raise InvalidPathError(f"Error: Rules file '{args.rules_path}' does not exist.")
    
    try:
        with open(args.output_path, 'w') as f:
            pass
    except OSError as e:
        raise InvalidPathError(f"Error: Output path '{args.output_path}' is not valid or writable. {str(e)}")

def run_pipeline(rules_path:str, csv_path:str, output_path:str):
    with open(rules_path, 'r') as f:
        rules = json.loads(f.read())
        
    cleaner = CSV_Cleaner(rules, csv_path)
    cleaner.load_data()
    cleaner.clean_data()

    cleaner.log_debug_info()   
    cleaner.save_data(output_path)
    
    validator = CSV_Validator(rules, data=cleaner.pandas)
    log = validator.validate_data()
    
    logging.info(Report.gen_validation_log(log))

def setup_logging(verbose: int):
    if verbose == 0:
        level = logging.ERROR
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )

def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    
    try:
        validate_paths(args)
    except InvalidPathError as e:
        logging.critical(str(e))
        sys.exit(1)
        
    try:
        run_pipeline()
    
    except Exception as e:
        pass

if __name__ == "__main__":         
    main()

