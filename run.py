from toolkit.cleaner import CSV_Cleaner
from toolkit.validator import CSV_Validator
from toolkit.report_generator import Report
import json, argparse, os
import pandas as pd

parser = argparse.ArgumentParser(description='Clean and validate a CSV file based on provided rules.')
parser.add_argument('csv_path', type=str, help='Path to the CSV file to be cleaned and validated.')
parser.add_argument('rules_path', type=str, help='Path to the JSON file containing cleaning and validation rules.')
parser.add_argument('-o', '--output_path', type=str, help='Path to save the generated report.')
parser.add_argument('-r', '--report', action='store_true', help='Generate a report after cleaning and validation.')
parser.add_argument('--verbose', type=int, choices=[0, 1, 2], default=1, help='Set the verbosity level: 0 = no output, 1 = prints out information about the cleaned file, 2 = 1 and validation log.')

args = parser.parse_args()

if not os.path.exists(args.csv_path):
    print(f"Error: CSV file '{args.csv_path}' does not exist.")
    exit(1)

if not os.path.exists(args.rules_path):
    print(f"Error: Rules file '{args.rules_path}' does not exist.")
    exit(1)
    

if not args.output_path:
    args.output_path = input("Enter the path to save the report (e.g., 'report.txt'): ").strip()
    
while True:
    try:
        with open(args.output_path, 'w') as f:
            pass
        break
    
    except OSError as e:
        print(f"Error: Cannot write to '{args.output_path}'. {e}")
        args.output_path = input("Please enter a valid path to save the report: ").strip()
        
with open(args.rules_path, 'r') as f:
    rules = json.loads(f.read())
    
cleaner = CSV_Cleaner(rules, args.csv_path)
cleaner.load_data()
cleaner.clean_data()

if args.verbose >= 1:
    print("Cleaned Data:")
    print(cleaner.data_to_string)
    cleaner.pandas.info()

    
cleaner.save_data(args.output_path)
validator = CSV_Validator(rules, data=cleaner.pandas)
log = validator.validate_data()

if args.verbose >= 2:
    print("Validation executed on cleaned data.")
    print(Report.gen_validation_log(log))

