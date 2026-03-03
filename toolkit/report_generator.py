import pandas as pd

class Report:
    def __init__(self, df:pd.DataFrame, title:str="Report"):
        self.title = title
        self.df = df
        
    def gen_statistics(self):
        stats = "Statistics:\n"
        for col in self.df.columns:
            stats += f"\nColumn: {col}\n"
            stats += f"  - Non-null count: {self.df[col].count()}\n"
            stats += f"  - Unique values: {self.df[col].nunique()}\n"
            stats += f"  - Data type: {self.df[col].dtype}\n"
            if pd.api.types.is_numeric_dtype(self.df[col]):
                stats += f"  - Mean: {self.df[col].mean()}\n"
                stats += f"  - Median: {self.df[col].median()}\n"
                stats += f"  - Std Dev: {self.df[col].std()}\n"
                
        return stats

    @staticmethod
    def gen_validation_log(validation_log:dict):
        rep = ""
        ALIAS = {
                "missing_headers": "Missing Headers",
                "null_values": "Null Values",
                "numeric_errors": "Numeric Validation Errors",
                "datetime_errors": "Datetime Validation Errors",
                "email_errors": "Email Validation Errors",
                "duplicate_entries": "Duplicate Entries"
            }
            
        rep += f"Validation Log:\n"
        for key, value in validation_log.items():
            rep += f"\n{ALIAS[key]}:\n"
            
            if type(value) == list:
                for item in value:
                    rep += f"  - {item}\n"
                else: 
                    rep += f"  No issues found.\n"
                    
            elif type(value) == dict:
                for subkey, subvalue in value.items():
                    rep += f"  {subkey}:\n"
                    for idx in subvalue:
                        rep += f"    - Index {idx}\n"
            else:
                rep += f"  {value}\n"
                
        return rep

    def generate(self, include_statistics=True, clean_data=False, validation_log:dict=None, output_path:str=None):
        """Generates the report based on the CSV stored in self.df

        Args:
            include_statistics (bool, optional): Include statistics mean/median/std for every numeric column. Defaults to True.
            clean_data (bool, optional): Used to specify in the report if the data has been cleaned. Defaults to False.
            validation_log (dict, optional): Include the validation log. Defaults to None.
            output_path (str, optional): Store the report at the specified path, otherwise prints to stdout. Defaults to None.
        """
        rep = f"{self.title}\n\n"
        if clean_data:
            rep += "Report generated from cleaned CSV data.\n\n"
        
        rep += f"Number of rows: {len(self.df)}\n"
        rep += f"Number of columns: {len(self.df.columns)}\n"
        rep += f"Column names: {', '.join(self.df.columns)}\n"
        
        if include_statistics:
            rep += self.gen_statistics()
        
        if validation_log:
            rep += '\n'
            rep += self.gen_validation_log(validation_log)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(rep)
        else:
            print(rep)