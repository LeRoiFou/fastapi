def operation_complexe(valeur: int) -> str:
    """
    Indication du montant HT selon le montant TTC saisi
        :param valeur: nombre entier saisi par l'utilisateur
        :return: str du montant HT
    """
    
    return f"Montant HT : {int(valeur / 1.20)} €"
