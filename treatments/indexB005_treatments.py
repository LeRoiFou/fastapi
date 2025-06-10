def imc(weight: int, size: int) -> str:
    """
    Calcul de l'IMC = Poids / Taille²
        :param weight: poids de l'invidu en kg (nombre entier)
        :param size: taille de l'individu en cm (nombre entier)
        :return: détermination de l'IMC (str)
    """
    
    # Détermination de l'IMC = poids en kg / (taille en cm / 100)²
    imc_result = weight / (size / 100)**2
    
    # Selon le résultat obtenu...
    if imc_result < 16.5:
        return f"""Pour un poids de {weight} kg, et pour une taille de {size} cm, 
vous êtes dans la situation suivante : famine"""
    elif 16.5 <= imc_result < 18.5:
        return f"""Pour un poids de {weight} kg, et pour une taille de {size} cm, 
vous êtes dans la situation suivante : maigreur"""
    elif 18.5 <= imc_result < 25:
        return f"""Pour un poids de {weight} kg, et pour une taille de {size} cm, 
vous êtes dans la situation suivante : corpulence normale"""
    elif 25 <= imc_result < 30:
        return f"""Pour un poids de {weight} kg, et pour une taille de {size} cm, 
vous êtes dans la situation suivante : surpoids"""
    elif 30 <= imc_result < 35:
        return f"""Pour un poids de {weight} kg, et pour une taille de {size} cm, 
vous êtes dans la situation suivante : obésité modérée"""
    elif 35 <= imc_result < 40:
        return f"""Pour un poids de {weight} kg, et pour une taille de {size} cm, 
vous êtes dans la situation suivante : obésité sévère"""
    else:
        return f"""Pour un poids de {weight} kg, et pour une taille de {size} cm, 
vous êtes dans la situation suivante : obésité morbide ou massive"""
