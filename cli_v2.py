from toolkit.report_generator import Report
from cli import InvalidPathError, validate_paths, setup_logging, run_pipeline
from pathlib import PureWindowsPath
import argparse, sys, logging
import pandas as pd

def parse_arguments():
    parser = argparse.ArgumentParser(description='Clean and validate a CSV file based on provided rules.')
    parser.add_argument('task', type=str, choices=["clean", "explain"], help='The task to perform: "clean", "explain".')
    parser.add_argument('csv_path', type=str, help='Path to the CSV file to be cleaned and validated.')
    parser.add_argument('rules_path', type=str, help='Path to the JSON file containing cleaning and validation rules.')
    # parser.add_argument('-o', '--output_path', type=str, required=True, help='Path to save the cleaned file.')
    # parser.add_argument('-r', '--report', action='store_true', help='Generate a report after cleaning and validation.')
    parser.add_argument('--verbose', type=int, choices=[0, 1, 2], default=1, help='Set the verbosity level: 0 = no output, 1 = prints out information about the cleaned file, 2 = 1 and validation log.')

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    
    try:
        validate_paths(args)
        log, df = run_pipeline(args.rules_path, args.csv_path, args.csv_path)
        
    except InvalidPathError as e:
        logging.critical(str(e))
        sys.exit(1)
        
    except Exception as e:
        logging.critical(f"An unexpected error occurred.", exc_info=True)
        sys.exit(1)
    
    Report(df).generate(
        include_statistics=False,
        clean_data=True, validation_log=log,
        output_path=f"cache/report_{PureWindowsPath(args.csv_path).name}.txt")
                       
    if args.task == "explain":
        pass

if __name__ == "__main__":
    main()