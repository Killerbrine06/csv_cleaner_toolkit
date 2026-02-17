import pandas as pd

class CSV_Cleaner:
    def __init__(self, rules:dict, file_path:str):
        self.file_path = file_path
        self.__df = None
        self.__rules = rules

    def load_data(self):
        self.__df = pd.read_csv(self.file_path, skipinitialspace=True, skip_blank_lines=True)

    def clean_data(self):
        df = self.__df
        # Normalize column names
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.lower()

        # Strip whitespace from string columns
        string_cols = df.select_dtypes(include='str').columns
        df[string_cols] = df[string_cols].apply(lambda x: x.str.strip())

        # Replace empty strings with NaN
        df = df.replace(r'^\s*$', pd.NA, regex=True)

        # Drop rows with all NaN values
        df = df.dropna(how='all')

        self.__df = df
    
    @property
    def data_to_string(self):
        return self.__df.to_string()
    
    @property
    def pandas(self):
        return self.__df

    def fix_errors(self):
        pass
    
    def save_data(self, output_path:str):        
        self.__df.to_csv(output_path, index=False)