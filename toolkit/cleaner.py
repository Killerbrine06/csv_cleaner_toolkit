import io
import logging

import pandas as pd
import country_converter as cc

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
        
        # Drop duplicaate rows
        df = df.drop_duplicates()
        
        # Normalizing country names and dates
        for header in self.__rules['table']['headers']:
            if self.__rules['table']['headers'][header] == 'country':
                df[header] = df[header].apply(lambda x: cc.convert(names=x, to='ISO3', not_found=pd.NA) if pd.notna(x) else x)

            elif self.__rules['table']['headers'][header] == 'datetime':
                df[header] = pd.to_datetime(df[header], format="mixed", errors='coerce')
                df[header] = df[header].dt.strftime('%d/%m/%Y')
                        
        self.__df = df
    
    def log_debug_info(self):
        buffer = io.StringIO()
        self.__df.info(buf=buffer)
        logging.debug(buffer.getvalue())
            
    @property
    def pandas(self):
        return self.__df

    def fix_errors(self):
        pass
    
    def save_data(self, output_path:str):        
        self.__df.to_csv(output_path, index=False)