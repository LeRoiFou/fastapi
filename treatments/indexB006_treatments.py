import pandas as pd

def treatments(
    file_loaded: str, cr1: int, cr2: int, cr3: str, output_path: str) -> None:
    """
    Extraction par exclusions à partir du fichier Excel chargé
        :param file_loaded: fichier chargé
        :param cr1: salaires max à exclure (bas de la fourchette)
        :param cr2: salaires min à exclure (haut de la fourchette)
        :param cr3: civilité à exclure (monsieur ou madame)
        :param output_path: chemin et nom du fichier généré
        :return: désignation du chemin du fichier généré à récupérer
    """
    
    # Conversion du fichier Excel chargé en DF pandas
    tb = pd.read_excel(file_loaded, sheet_name='Feuil1')
    
    # Liste des données à exclure
    tb = tb.mask(
        (tb['Salaire'] < cr1) |
        (tb['Salaire'] > cr2) |
        (tb['Civilité'] == cr3)
    ).dropna().sort_values(by=['Salaire'], ascending=True
                           ).reset_index(drop=True)
    
    # Exportation des données sous format Excel sans les index
    tb.to_excel(output_path, index=False)
    
    return output_path

    
# mask('data/Mask.xlsx', 2000, 2500, 'Monsieur')