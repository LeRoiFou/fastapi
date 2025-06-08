"""
Fichier test des scripts opérés avec la librairie Fastapi

Installer les librairies pytest et requests : 
- pip install pytest
- pip install requests

Puis saisir dans le terminal : pytest indexA003_test_file.py 
(ici indexA003_test_file.py = nom du fichier ici)

Ceci permet de vérifier le succès ou l'échec du script saisi
"""

from fastapi.testclient import TestClient

# Modularité : récupération de la variable app du fichier test_file.py
from indexA003_test_file import app 

# Instanciation de la sous-librairie TestClient en alimentant la variable app
# du fichier test_file.py
client = TestClient(app)

def test_read_root():
    """
    Vérification si le retour est de code HTML 200
    """
    
    # Test sur la fonction read_route() du fichier test_file.py qui est un GET
    response = client.get('/')
    
    # Vérification si le script est correct :
    # L'instruction assert en Python sert à vérifier qu'une condition est vraie 
    # à un moment donné dans le code. 
    # Si la condition est fausse, Python lève automatiquement une exception 
    # de type AssertionError, ce qui permet de détecter rapidement 
    # des erreurs ou des incohérences pendant le développement
    assert response.status_code == 200
    # assert response.status_code == 500 , 'Erreur dans le script !'
    
    # Réponse attendu du script de la fonction read_route() du fichier test_file.py
    assert response.json() == {'Message': 'Hello World!'}
