from toolkit.cleaner import CSVCleaner
from toolkit.validator import CSVValidator
from toolkit.report_generator import Report
import json, argparse, os, sys, logging

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
        output_dir = os.path.dirname(args.output_path) or "."
        if not os.path.isdir(output_dir):
            raise InvalidPathError(f"Error: Output directory '{output_dir}' does not exist.")
    
    except AttributeError:
        pass

def summarise(log:dict):
    total_nulls = sum(len(v) for v in log["null_values"].values())
    total_numeric = sum(len(v) for v in log["numeric_errors"].values())
    
    logging.info(
        "Validation summary: "
        "%d missing headers | "
        "%d null values across %d columns | "
        "%d numeric errors | "
        "%d invalid emails | "
        "%d duplicate rows",
        len(log["missing_headers"]),
        total_nulls,
        len(log["null_values"]),
        total_numeric,
        sum(len(v) for v in log["email_errors"].values()),
        sum(len(v) for v in log["duplicate_entries"].values())
    )
    logging.debug(log)
    # logging.debug(json.dumps(log, indent=2))

def run_pipeline(rules_path:str, csv_path:str, output_path:str) -> dict:
    with open(rules_path, 'r') as f:
        rules = json.load(f)
        
    cleaner = CSVCleaner(rules, csv_path)
    cleaner.load_data()
    cleaner.clean_data()

    cleaner.log_debug_info()   
    cleaner.save_data(output_path)
    
    logging.info("Cleaned data loaded successfully.")
    logging.info("Rows: %d | Columns: %d", cleaner.pandas.shape[0], cleaner.pandas.shape[1])
    
    validator = CSVValidator(rules, data=cleaner.pandas)
    log = validator.validate_data()
    summarise(log)
    
    return log
    

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
        log = run_pipeline(args.rules_path, args.csv_path, args.output_path)
    except InvalidPathError as e:
        logging.critical(str(e))
        sys.exit(1)
    
    except Exception as e:
        logging.critical(f"An unexpected error occurred.", exc_info=True)
        sys.exit(1)
        
if __name__ == "__main__":         
    main()
