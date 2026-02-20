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

    def generate(self, include_statistics=True, clean_data=False, validation_log:str=None, output_path:str=None):
        rep = f"{self.title}\n\n"
        if clean_data:
            rep += "Report generated from cleaned CSV data.\n\n"
        
        rep += f"Number of rows: {len(self.df)}\n"
        rep += f"Number of columns: {len(self.df.columns)}\n"
        rep += f"Column names: {', '.join(self.df.columns)}\n"
        
        if include_statistics:
            rep += self.gen_statistics()
        
        if validation_log:
            with open(validation_log, 'r') as log_file:
                rep += f"\nValidation Log:\n{log_file.read()}\n"
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(rep)
        else:
            print(rep)