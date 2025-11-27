import os
import polars as pl
import pandas as pd

def department():
    # path and name of the Python file used here :
    # c:\Users\LRCOM\Documents\Professionnel\Python\fastapi\treatments
    base = os.path.dirname(os.path.abspath(__file__))

    # Retrieve Excel file to loaded
    excel_file = os.path.join(base, '../input/Departements.xlsx')
    
    # File excel loaded
    df = pd.read_excel(str(excel_file))
    
    # New column
    df['Departement'] = df['Numero'].astype('str') + " - " + df['Département']
    
    # Convert DF pandas to list
    department_list = df['Departement'].to_list()
    
    return department_list

def city(department: str) -> list:

    # path and name of the Python file used here :
    # c:\Users\LRCOM\Documents\Professionnel\Python\fastapi\treatments
    base = os.path.dirname(os.path.abspath(__file__))

    # Retrieve Excel file to loaded
    excel_file = os.path.join(base, '../input/Secteur.xlsx')

    # File excel loaded
    df = pd.read_excel(str(excel_file))
    
    # Convert department field to string
    df['DEPARTEMENT'] = df['DEPARTEMENT'].astype('str')
    
    # Department selected
    df = df[df['DEPARTEMENT'] == department]
    
    # Unique value for COMMUNE fied
    df = df['COMMUNE'].unique()
    
    return df.tolist()
    
def prefix(city):
    
    # path and name of the Python file used here :
    # c:\Users\LRCOM\Documents\Professionnel\Python\fastapi\treatments
    base = os.path.dirname(os.path.abspath(__file__))

    # Retrieve Excel file to loaded
    excel_file = os.path.join(base, '../input/Secteur.xlsx')

    # Excel file converted to DF polars
    df = pl.read_excel(str(excel_file)).fill_null('').lazy()
    
    prefix_df = df.filter(pl.col('COMMUNE').str.contains(city)).collect()
    
    prefix_df = (prefix_df
                 .select(pl.col('SECTION'))
                 .unique()
                 .cast(pl.Int32)
                 .sort(by='SECTION')
                 )

    prefix_list = prefix_df['SECTION'].to_list()
    
    return prefix_list
    