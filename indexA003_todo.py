from fastapi import FastAPI, HTTPException
import uvicorn
from typing import List
from pydantic import BaseModel

# Instanciation de la sous-librairie FastApi
app = FastAPI(title='TODO API', version='V1')

# Classe héritant de la sous-librairie BaseModel de pydantic
class Todo(BaseModel):
    """
    Typage affecté à chaque variable déclarée
    """
    name: str
    due_date: str
    description: str

# Assignation d'une liste  
store_todo = []

# Route POST : saisie des données à la page spécifiée à l'URL (C.R.U.D. -> CREATE)
@app.post('/todo') # URL
async def create_todo(todo: Todo):
    """
        :param todo: arguments avec typage déclaré dans la classe Todo
        :return: MAJ de la liste store_doto
    """
    # Ajout des variables de la classe Todo dans la liste store_doto
    store_todo.append(todo)
    
    return store_todo

# Route GET : accès à la page spécifiée à l'URL (C.R.U.D. -> READ)
@app.get('/todos/', # URL
         response_model=List[Todo], # Typage à sortir des variables de la classe Todo
         ) 
async def get_all_todos():
    """
        :return: Accès de la liste store_todo
    """
    return store_todo

# Route GET : accès à la page spécifiée à l'URL (C.R.U.D. -> READ)
@app.get('/todo/{id}') # URL avec saisi un nombre entier
async def get_todo(id: int):
    """
        :param id: nombre entier
        :return: affichage du composant de la liste store_doto selon l'ID saisi dans l'URL
    """
    try:
        return store_todo[id]
    except:
        # Erreur non trouvée (code HTTP 404) 
        # si le composant saisi n'est pas dans la liste store_doto
        raise HTTPException(status_code=404, detail='Todo not found database')

# Route PUT : MAJ (C.R.U.D. -> UPDATE)
@app.put('/todo/{id}') # URL avec saisi d'un nombre entier
async def update_todo(id: int, new_todo: Todo):
    """
        :param id: nombre entier
        :param new_todo: typage des variables déclarées dans la classe Todo
        :return: modification des variables déclarées selon le composant sélectionné dans la liste store_doto
    """
    try:
        # N° de composant ciblé pour modifier les variables
        store_todo[id] = new_todo
        
        return store_todo[id]
    
    except:
        # Erreur non trouvée (code HTTP 404)
        # si le composant saisi n'est pas dans la liste store_doto
        raise HTTPException(status_code=404, detail='Todo not found database')
    
# Route DELETE : suppression (C.R.U.D. -> DELETE)
@app.delete('/todo/{id}') # URL avec saisi d'un nombre entier
async def delete_todo(id: int):
    """
        :param id: nombre entier
        :return: suppression des variables du composant sélectionné de la liste store_todo
    """
    try:
        # Sélection du composant de la liste store_doto
        obj = store_todo[id]
        
        # Suppression des variables du composant sélectionné
        store_todo.pop(id)
        
        return obj
    
    except:
        # Erreur non trouvée (code HTTP 404)
        # si le composant saisi n'est pas dans la liste store_doto
        raise HTTPException(status_code=404, detail='Todo not found database')
    

if __name__ == '__main__':
    
    # Lancement automatique du serveur local sans rien saisir dans le terminal
    uvicorn.run(app)
