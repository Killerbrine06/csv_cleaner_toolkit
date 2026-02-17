import pandas as pd

class CSV_Validator:
    def __init__(self, rules:dict, log_path:str, file_path:str=None, data=None):
        if not (file_path or type(data) == pd.DataFrame):
            raise ValueError("Either file_path or data must be provided.")
            
        self.log_path = log_path
        if type(data) == pd.DataFrame:
            self.__df = data
            self.file_path = None
        else:
            self.__df = None
            self.file_path = file_path
            
        self.__rules = rules

    def load_data(self):
        self.__df = pd.read_csv(self.file_path, skipinitialspace=True, skip_blank_lines=True)

    def validate_data(self):
        log_file = open(self.log_path, 'w')
        
        # Not Null validation
        for header, def_value in self.__rules['table']['not_null_entries']:
            header = header.strip().replace(' ', '_').lower()
            
            if header not in self.__df.columns:
                log_file.write(f"Missing header: {header}\n")
                continue
            
            null_rows = self.__df[header].isna()
            if null_rows.any():
                log_file.write(f"Null values found in header '{header}':\n")
                for idx in self.__df[null_rows].index:
                    log_file.write(f"Row {idx}\n")
        
        for header in self.__rules['table']['headers']:
            header = header.strip().replace(' ', '_').lower()
            
            if header not in self.__df.columns:
                log_file.write(f"Missing header: {header}\n")
                continue
            
            # Numeric validation
            if self.__rules['table']['headers'][header] in ['float', 'int']:
                cols_to_num = pd.to_numeric(self.__df[header], errors='coerce')
                bad_rows = cols_to_num.isna() & self.__df[header].notna()
                
                if bad_rows.any():
                    log_file.write(f"Non-numeric values in header '{header}':\n")
                    for idx in self.__df[bad_rows].index:
                        log_file.write(f"Row {idx}: {self.__df.loc[idx, header]}\n")
                        
            # Datetime validation
            if self.__rules['table']['headers'][header] == 'datetime':
                cols_to_date = pd.to_datetime(self.__df[header], format="mixed", errors='coerce')
                bad_rows = cols_to_date.isna() & self.__df[header].notna()
                
                if bad_rows.any():
                    log_file.write(f"Invalid datetime values in header '{header}':\n")
                    for idx in self.__df[bad_rows].index:
                        log_file.write(f"Row {idx}: {self.__df.loc[idx, header]}\n")
                        
            # Email validation
            if self.__rules['table']['headers'][header] == 'email':
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                bad_rows = ~self.__df[header].str.match(email_pattern, na=False)
                
                if bad_rows.any():
                    log_file.write(f"Invalid email values in header '{header}':\n")
                    for idx in self.__df[bad_rows].index:
                        log_file.write(f"Row {idx}: {self.__df.loc[idx, header]}\n")
                    
        log_file.close()
            