from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import uvicorn

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Instanciation en variable du dossier templates récupéré (fichiers HTML récupérés)
templates = Jinja2Templates(directory='templates')

# Handler personnalisé pour les erreurs de validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Vérifie si la requête vient d’un formulaire
    if request.headers.get("content-type", "").startswith(
        "application/x-www-form-urlencoded"):
        return templates.TemplateResponse(
            "indexB004.html",  # template HTML
            {
                "request": request,
                "message_erreur": "Veuillez entrer un nombre entier valide !",
            },
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        )
    # Sinon, comportement JSON par défaut
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Erreur de validation", "errors": exc.errors()},
    )

@app.get('/hello', # URL avec chemin spécifié
         response_class=HTMLResponse, # affichage en HTML
         summary="Page HTML à afficher par défaut",
         description="""
         Retour de la page HTML par défaut
         
         param request: à mentionner sinon erreur
         """,
         )
async def get_hello(request:Request):
    return templates.TemplateResponse(
        'indexB004.html', # accès au fichier HTML
        {'request': request, 'message': ''}, # Données à restituer
        )
    
@app.post('/hello', # URL avec chemin spécifié
         response_class=HTMLResponse, # affichage en HTML
         summary="Page HTML avec restitution des données saisies",
         description="""
         Retour de la page HTML avec données saisies par l'utilisateur
         
         param request: à mentionner sinon erreur
         args message: données saisies par l'utilisateur
         """,
         )
async def post_hello(request: Request, message: int = Form(...)) -> str:
    return templates.TemplateResponse(
        'indexB004.html', # accès au fichier HTML
        {'request': request, 'message': message}, # Données à restituer
        )


if __name__ == '__main__':
    
    # Lancement du serveur local
    uvicorn.run(app)
