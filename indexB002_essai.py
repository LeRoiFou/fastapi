from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Accès aux fichiers HTML du répertoire templates
templates = Jinja2Templates(directory='templates')

# Permet d'accéder aux fichiers CSS du dossier static/
app.mount('/static/', StaticFiles(directory='static'), name='static')

@app.get('/hello', # URL avec chemin spécifié
         response_class=HTMLResponse, # affichage en HTML
         summary="Page par défaut au format HTML",
         description="""
         Retour des données au format HTML
         
         Param request : données à restituer
         """,
         )
async def get_hello(request:Request):
    return templates.TemplateResponse(
        'indexB002.html', # récupération des données du fichier HTML
        {'request': request, 'message': '💀💀💀 ❓'} # message par défaut
    )
    
@app.post('/hello', # URL avec chemin spécifié
         response_class=HTMLResponse, # affichage en HTML
         summary="Modification du message à afficher après le bouton appuyé",
         description="""
         Retour des données au format HTML
         
         Param request : données à restituer
         """,
         )
async def post_hello(request:Request):
    
    # Instanciation du message à afficher
    message = "Hello World!"
    
    return templates.TemplateResponse(
        'indexB002.html', # récupération des données du fichier HTML
        {'request': request, 'message': message} # données à restituer
    )

if __name__ == '__main__':
    uvicorn.run(app)
