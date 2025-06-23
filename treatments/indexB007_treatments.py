import polars as pl

def treatments(upload_file):
    """
    Traitements opérés sur le fichier Excel chargé
    
        :param upload_file: fichier chargé
        :return: traitements opérés sur la DF polars
    """
    
    # Récupération du fichier Excel converti en DF polars
    df = pl.read_excel(upload_file)
    
    # Regroupage en valeurs uniques converties en liste par ordre croissant
    return df['Civilité'].unique().sort().to_list()
