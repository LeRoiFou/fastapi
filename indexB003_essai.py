from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Instanciation dans une variable de l'accès au répertoire HTML
templates = Jinja2Templates(directory='templates')

@app.get('/hello', # URL avec chemin spécifié
         response_class=HTMLResponse, # Accès à la page HTML
         summary="Accès aux données au format HTML par défaut",
         description="""
         Retour des données au format HML
         
         param request: données à restituer
         """,)
async def get_hello(request: Request):
    return templates.TemplateResponse(
        'indexB003.html', # récupération des données du fichier HTML
        {'request': request, 'message': '❓'}) # Données à restituer
    
@app.post('/hello', # URL avec chemin spécifié
         response_class=HTMLResponse, # Accès à la page HTML
         summary="Modification du message à afficher après le bouton appuyé",
         description="""
         Retour des données au format HML
         
         param request: données à restituer
         args message: zone de saisie pour l'utilisateur
         """,)
async def post_hello(request: Request, message: str = Form(...)) -> str:
    return templates.TemplateResponse(
        'indexB003.html', # récupération des données du fichier HTML
        {'request': request, 'message': f'Hello {message}'}) # Données à restituer

if __name__ == '__main__':
    
    # Lancement direct sans saisir quoique ce soit dans le terminal
    uvicorn.run(app)
