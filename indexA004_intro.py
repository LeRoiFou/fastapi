import json
from dataclasses import dataclass, asdict
from typing import Union
from fastapi import FastAPI, Path, HTTPException
import uvicorn

#===== Structure de données : Dictionnaire indexé par pokemon id =====#

# Récupération des données du fichier pokemons.json converti en une liste de
# dictionnaires
with open("data/pokemons.json", "r") as f:
    pokemons_list = json.load(f)

# Conversion de la liste de dictionnaire en un seul dictionnaire
list_pokemons = {k+1:v for k, v in enumerate(pokemons_list)}


#===== Déclaration des attributs d'un pokemon =====#

@dataclass
class Pokemon() :
    """
    Les dataclasses permettent de déclarer des attributs sans passer par un
    constructeur.
    
    Ici on déclare les attributs d'un Pokemon
    """
    id: int
    name: str
    types: list[str]
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    evolution_id: Union[int, None] = None # un pokemon peut évoluer ou pas
    
# ======================================================================

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

@app.get('/total_pokemons', # URL avec un chemin spécifié
         summary="Accès au nombre total de pokemons",
         description="""Retour d'un dictionnaire avec la longueur totale de la liste 
         des pokemons""",
         ) 
async def get_total_pokemons() -> dict:
    return {'total': len(list_pokemons)}

@app.get('/all_pokemons', # URL avec un chemin spécifié
         summary="Récupérer tous les pokemons",
         description="Retour de la liste de tous les pokemons",
         ) 
async def get_all_pokemons() -> list[Pokemon]:
    # Assignation d'une liste vide
    res = []
    
    # Compréhension de liste : conversion d'un dictionnaire en objet à partir
    # de la dataclasse Pokemon
    [res.append(Pokemon(**list_pokemons[id])) for id in list_pokemons]
    
    return res

@app.get('/one_pokemon/{id}', # URL avec un chemin spécifié
         summary="Récupérer un pokemon avec l'ID ciblé",
         description="""
         Retour de la classe Pokemon instanciée avec les données du pokemon selon 
         l'ID ciblé
         
         argument id : n° ID pokemon saisi (nombre entier) avec au minimum la valeur 1
         """,
         ) 
async def get_one_pokemon(id: int = Path(ge=1)) -> Pokemon:   
    # Si le n° ID saisi n'est pas dans la liste list_pokemons...
    if id not in list_pokemons:
        raise HTTPException(status_code=404,
                            detail="Ce pokemon n'existe pas...")
    
    return Pokemon(**list_pokemons[id])

@app.post('/create_pokemon/', # URL avec un chemin spécifié
          summary="Créer un pokemon",
          description="""
          Retour de la classe Pokemon instanciée avec les nouvelles données saisies
          
          param pokemon : pokemon créé à partir du modèle de la classe Pokemon
          """,
          ) 
async def post_create_pokemon(pokemon: Pokemon) -> Pokemon:    
    # Si le n° ID saisi existe déjà...
    if pokemon.id in list_pokemons :
        raise HTTPException(
            status_code=404,
            detail=f"Le pokemon avec l'ID {pokemon.id} existe déjà...")
    
    # Ajout dans la liste des pokemons  
    list_pokemons[pokemon.id] = asdict(pokemon)
    
    return pokemon

@app.put('/update_pokemon/{id}',  # URL avec un chemin spécifié
         summary="Modification des données d'un pokemon à partir d'un ID",
         description="""
            Retour de la classe Pokemon instanciée avec les données du pokemon 
            selon l'ID ciblé
         
            param pokemon : pokemon modifié à partir du modèle de la classe Pokemon
            
            argument id : n° ID pokemon saisi (nombre entier) avec au min la valeur 1
         """,
         )
async def put_update_pokemon(pokemon: Pokemon, id: int = Path(ge=1)) -> Pokemon:   
    # Si le n° ID saisi n'est pas dans la liste list_pokemons...
    if id not in list_pokemons:
        raise HTTPException(status_code=404,
                            detail="Ce pokemon n'existe pas...")
    
    # Modification dans la liste des pokemons  
    list_pokemons[id] = asdict(pokemon)
    
    return pokemon

@app.delete('/delete_pokemon/{id}', # URL avec chemin spécifié
            summary="Suppression d'un pokemon 💀",
            description="""
            Retour du pokemmon récupéré dans la liste list_pokemons
            
            argument id : n° ID pokemon saisi (nombre entier) avec au min la valeur 1
            """,
            )
async def delete_pokemon(id: int = Path(ge=1)) -> Pokemon:
    # Si l'ID saisi est dans la liste list_pokemons...
    if id in list_pokemons:
        # Instanciation des données du pokemon ciblé avec son ID
        pokemon = Pokemon(**list_pokemons[id])
        
        # Suppression du pokemon dans la liste list_pokemons
        del list_pokemons[id]
        
        return pokemon
    
    # A défaut si l'ID du pokemon n'existe pas...
    else:
        raise HTTPException(status_code=404,
                            detail="Ce pokemon n'existe pas...")
        
@app.get('/pokemon_types/',
         summary="Récupérer tous les types de pokemon (eau, feu...)",
         description="Retour d'une liste de chaîne de caractères",
         )
async def get_pokemon_types() -> list[str]:
    
    # Assignation d'une liste
    types = []
    
    # Ajout des différents types de pokemon dans la liste instanciée ci-avant
    for pokemon in pokemons_list:
        for type in pokemon['types']:
            if type not in types:
                types.append(type)
    
    # Trie croissant des types de pokemon          
    types.sort()
    
    return types

if __name__ == '__main__':
    
    # Lancement direct de l'appli sans saisir quoique ce soit dans le terminal
    uvicorn.run(app)
