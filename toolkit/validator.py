import pandas as pd

class CSV_Validator:
    def __init__(self, rules:dict, file_path:str=None, data=None):
        if not (file_path or type(data) == pd.DataFrame):
            raise ValueError("Either file_path or data must be provided.")
            
        if type(data) == pd.DataFrame:
            self.__df = data
            self.file_path = None
        else:
            self.__df = None
            self.file_path = file_path
            
        self.__rules = rules

    def load_data(self):
        self.__df = pd.read_csv(self.file_path, skipinitialspace=True, skip_blank_lines=True)

    def validate_data(self) -> dict:
        log = {"missing_headers": [], "null_values": {}, "numeric_errors": {}, "email_errors": {}, "duplicate_entries": {}}
        
        # Not Null validation
        for header, def_value in self.__rules['table']['not_null_entries']:
            header = header.strip().replace(' ', '_').lower()
            
            if header not in self.__df.columns:
                log["missing_headers"].append(header)
                continue
            
            null_rows = self.__df[header].isna()
            if null_rows.any():
                log["null_values"][header] = self.__df[null_rows].index.tolist()
        
        for header in self.__rules['table']['headers']:
            header = header.strip().replace(' ', '_').lower()
            
            if header not in self.__df.columns:
                log['missing_headers'].append(header)
                continue
            
            # Numeric validation
            if self.__rules['table']['headers'][header] in ['float', 'int']:
                cols_to_num = pd.to_numeric(self.__df[header], errors='coerce')
                bad_rows = cols_to_num.isna() & self.__df[header].notna()
                
                if bad_rows.any():
                    log["numeric_errors"][header] = self.__df[bad_rows].index.tolist()
                                                
            # Email validation
            if self.__rules['table']['headers'][header] == 'email':
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                bad_rows = ~self.__df[header].str.match(email_pattern, na=False)
                
                if bad_rows.any():
                    log["email_errors"][header] = self.__df[bad_rows].index.tolist()
                        
        # Unique entries validation
        for header in self.__rules['table']['unique_entries']:
            header = header.strip().replace(' ', '_').lower()
            
            if header not in self.__df.columns:
                log['missing_headers'].append(header)
                continue
            
            duplicates = self.__df[header][self.__df[header].duplicated(keep=False)]
            if not duplicates.empty:
                log["duplicate_entries"][header] = duplicates.index.tolist()
    
        return log    