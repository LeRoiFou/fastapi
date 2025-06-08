from fastapi import FastAPI
import uvicorn # pour le lancement automatique sans saisir dans le terminal
from typing import Optional # optionnel du typage attendu
from pydantic import BaseModel # voir fichier README.MD

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Route GET : accès à la page
@app.get('/')
async def hello_world():
    """
        :return: affichage du texte en type dictionnaire
    """ 
    # Message à afficher
    return {"Hello": "World"}

# Route GET : accès à la page spécifiée dans l'URL
@app.get('/component/{component_id}')
async def get_component(component_id: int):
    """
        :param: nombre entier saisi dans l'URL
        :return: affichage en dictionnaire du nombre entier saisi
    """  
    # Retour du n° entier saisi dans l'URL
    # A saisir en URL par ex : component/5
    return {'component_id': component_id}

# Route GET : accès à la page spécifiée dans l'URL
@app.get('/component_choice/')
async def read_component(number: int, text: str):
    """
        :param: nombre entier et texte saisi dans l'URL
        :return: affichage en dictionnaire du nombre entier et du texte saisi
    """
    # Retour du n° entier OU du texte saisi dans l'URL :
    # A saisir en URL par ex : /component_choice/?number=2&text=essai
    return {'number': number, 'text': text}

# Route GET : accès à la page spécifiée dans l'URL
@app.get('/component_optional/')
async def read_component(number: int, text: Optional[str]):
    """
        :param: nombre entier et texte (quelque soit le type) saisi
        :return: affichage en dictionnaire du nombre entier et du texte saisi
    """
    # Retour du n° entier OU du texte saisi dans l'URL :
    # A saisir en URL par ex : /component_optional/?number=2&text=3
    # ou à saisir en URL par ex : /component_optional/?number=2&text=
    # le retour de typage pour 'text' peut être en str grâce à la librairie Optional
    return {'number': number, 'text': text}


class Coord(BaseModel):
    """
    Classe héritant de la sous-librairie BaseModel de pydantic
    """
    lat: float
    lon: float
    zoom: Optional[int] # nombre entier en option
    
# Route POST : saisie de données
@app.post('/position/')
async def make_position(coord: Coord):
    """
        :param coord: arguments avec typage déclaré dans la classe Coord
        :return: données saisies sous la forme d'un dictionnaire
    """
    
    # Aller sur /docs dans l'URL et puis sur POST concerné pour contrôler
    return {"new coord": coord}

# Route POST : saisie de données
@app.post('/position_priority/')
async def make_position_priority(priority: int, coord: Coord):
    """
        :param priority: nombre entier saisi dans l'URL
        :param coord: arguments avec typage déclaré dans la classe Coord
        :return: données saisies sous la forme d'un dictionnaire
    """
    
    # Aller sur /docs dans l'URL et puis sur POST concerné pour contrôler
    return {'priority': priority, 'new coord': coord}

# Route POST : saisie de données
@app.post('/position_priority_value/')
async def make_position_priority_value(priority: int, coord: Coord, value: bool):
    """
        :param priority: nombre entier saisi dans l'URL
        :param coord: arguments avec typage déclaré dans la classe Coord
        :param value: booléen saisi dans l'URL
        :return: données saisies sous la forme d'un dictionnaire
    """
    # Aller sur /docs dans l'URL et puis sur POST concerné pour contrôler
    return {'priority': priority, 'new coord': coord, 'value': value}


class CoordIn(BaseModel):
    """
    Classe héritant de la sous-librairie BaseModel de pydantic
    """
    password: str
    lat: float
    lon: float
    zoom: Optional[int] = None # Soit un entier, soit rien
    description: Optional[str] = None # Soit un str, soit rien
    
class CoordOut(BaseModel):
    """
    Classe héritant de la sous-librairie BaseModel de pydantic
    """
    lat: float
    lon: float
    zoom: Optional[int] = None # Soit un entier, soit rien
    description: Optional[str] = None # Soit un str, soit rien
    
    
# Route POST : saisie de données
@app.post('/position_coordOut/', # URL
          response_model=CoordOut, # Arguments à sortir de la classe CoordOut
          )
async def make_position_coordOut(coord: CoordIn):
    """
    L'argument response_model permet d'avoir des données de sorties différentes que les données entrées (ici le MDP saisi ne s'affiche pas en sortie)
        :param coord: arguments avec typage déclaré dans la classe CoordIn
        :return: données saisies sous la forme d'un dictionnaire à partir de la classe CoordOut
    """
    
    # Aller sur /docs dans l'URL et puis sur POST concerné pour contrôler la sortie
    return CoordOut(
        lat=coord.lat, lon=coord.lon, zoom=coord.zoom, description=coord.description)

# Route POST saisie de données
@app.post('/position_include', # URL
          response_model=CoordOut, # Arguments à sortir de la classe CoordOut
          response_model_include={'description'}, # Arguments à inclure en sortie
          )
async def make_position_include(coord: CoordIn):
    """
    L'argument response_mode permet d'avoir des données de sorties différentes que les données entrées (ici le MDP saisi ne s'affiche pas en sortie)
        :param coord: arguments avec typage déclaré dans la classe CoordIn
        :return: données saisies sous la forme d'un dictionnaire à partir de la classe CoordOut
    """
    
    # Aller sur /docs dans l'URL et puis sur POST concerné pour contrôler la sortie
    return CoordOut(
        lat=coord.lat, lon=coord.lon, zoom=coord.zoom, description=coord.description)

# Route POST saisie de données   
@app.post('/position_exclude', # URL
          response_model=CoordOut, # Arguments à sortir de la classe CoordOut
          response_model_exclude={'lon'}, # Argument à exclure en sortie
          )
async def make_position_exclude(coord: CoordIn):
    """
     L'argument response_mode permet d'avoir des données de sorties différentes que les données entrées (ici le MDP saisi ne s'affiche pas en sortie)
        :param coord: arguments avec typage déclaré dans la classe CoordIn
        :return: données saisies sous la forme d'un dictionnaire à partir de la classe CoordOut 
    """
    
    # Aller sur /docs dans l'URL et puis sur POST concerné pour contrôler la sortie
    return CoordOut(
        lat=coord.lat, lon=coord.lon, zoom=coord.zoom, description=coord.description)
    

if __name__ == '__main__':
    
    # Lancement automatique du serveur local sans rien saisir dans le terminal
    uvicorn.run(app, host='127.0.0.1', port=8000)
