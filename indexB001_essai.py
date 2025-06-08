from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Indique à FastAPI d’aller chercher les fichiers .HTML au dossier templates
templates = Jinja2Templates(directory="templates")

# Permet d'accéder aux fichiers du dossier static/ via l'URL /static/
app.mount('/static/', StaticFiles(directory='static'), name='static')

@app.get(
    '/hello', # URL avec un chemin specifié
    response_class=HTMLResponse, # affichage en HTML
    summary="Récupération des données d'un fichier HTML",
    description="""
    Retour des données au format HTML
    
    Param request : à inclure si on a recours au HTML même si aucune requête n'est effectuée
    """,
    )
async def hello_world(request:Request):
    return templates.TemplateResponse(
        'indexB001.html', # récupération des données du fichier HTML
        {"request": request}, # à inclure sinon erreur
        )

if __name__ == '__main__':
    
    # Evite de saisir quoique ce soit dans le terminal
    uvicorn.run(app)
