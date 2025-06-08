from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Accès aux fichiers HTML du répertoire templates
templates = Jinja2Templates(directory='templates')

@app.get('/hello', # URL avec chemin spécifié
         response_class=HTMLResponse, # affichage en HTML
         summary="Accès des données au format HTML",
         description="""
         Retour des données au format HTML
         
         Param request : données à restituer
         """,
         )
async def get_hello(request:Request):
    return templates.TemplateResponse(
        'indexB002.html', # récupération des données du fichier HTML
        {'request': request, 'message': '❓'} # données à restituer
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
