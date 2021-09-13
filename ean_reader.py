import pandas as pd

def read_file(file=None, filename=None, sheets=None):
    """
    accepts a bytefile or filename as csv or excel and returns a list of product identifiers
    tries to merge all sheets in excel files unless sheets are specified - look up pandas.read_excel for accepted inputs
    """
    if not filename:
        filename = file.filename
    else:
        file=filename
        
    if filename[-3:]=="csv":
        # loops through several possible read configurations until the dataframe looks usable
        csv_configs = {"separator":[";", "\t", "|", ","],
                        "encoding":["latin1", "utf-8", "iso-8859-1", "cp1252"],
                        "skip_errors":["error", "skip"]}
        found = False
        for config in itertools.product(*csv_configs.values()):
            file.seek(0)
            if found == True:
                break
            try:
                df = pd.read_csv(file, sep=config[0], encoding=config[1], on_bad_lines=config[2])
                if (len(df.columns) == 1) & (len(df.columns[0]) > 10):
                    raise pd.errors.ParserError
                found = True
            except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError):
                pass
    elif filename[-4:]=="xlsx":
        print("found excel")
        dfs = pd.read_excel(file, sheet_name=sheets)
        df = pd.DataFrame()
        for name,data in dfs.items():
            df = df.append(data, sort=False)
    return df

def get_eans(df, ean_names=["ean", "eans", "gtin", "gtins"]):
    for col in df.columns:
        if str(col).lower() in ean_names:
            df = df.dropna(subset=[col])
            eans = df[col].astype(str).apply(lambda x: x.replace(".0",""))
            eans = eans.drop_duplicates().reset_index(drop=True)
            return eans
    return "No ean column found"