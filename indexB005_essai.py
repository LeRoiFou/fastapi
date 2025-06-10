from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

from treatments import indexB005_treatments

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Assignation du variable récupérant le répertoire templates (fichiers HTML)
templates = Jinja2Templates(directory='templates')

# Récupération du répertoire static compreant les fichiers CSS
app.mount('/static/', StaticFiles(directory='static'), name='static')

@app.get('/', # URL avec chemin spécifié
         response_class=HTMLResponse, # affichage en HTML
         summary="Calcul de l'IMC",
         description="""
         Retour de l'affichage par défaut
         
         param request: requêtes à saisir directement dans le fichier HTML
         """,
         )
async def get_imc(request: Request):
    return templates.TemplateResponse(
        'indexB005.html', # accès au fichier HTML
        { # Données à restituer
            'request': request, # requêtes à saisir directement dans le fichier HTML
            'message': '', # message à restituer
            'message_error': '', # message d'erreur à restituer
        },
    )
    
@app.post('/', # URL avec chemin spécifié
         response_class=HTMLResponse, # affichage en HTML
         summary="Calcul de l'IMC",
         description="""
         Retour de l'IMC
         
         param request: requêtes à saisir directement dans le fichier HTML
         args message: saisie dans la zone de texte par l'utilisateur
         """,
         )
async def post_imc(request: Request, weight: str=Form(...), size: str=Form()) -> str:
    
    try:
        # Conversion des données saisies en type int
        weight_int = int(weight)
        size_int = int(size)
        
        # Résultat des données saisies
        imc_result = indexB005_treatments.imc(weight_int, size_int)
        
        return templates.TemplateResponse(
            'indexB005.html', # accès au fichier HTML
            { # Données à restituer
                'request': request, # requêtes à saisir directement dans le fichier HTML
                'message': imc_result, # message à restituer
                'message_error': '', # message d'erreur à restituer
            },
        )
    
    # Si la saisie des données par l'utilisateur ne sont pas des entiers numériques
    except ValueError:
        return templates.TemplateResponse(
            'indexB005.html', # accès au fichier HTML
            { # Données à restituer
                'request': request, # requêtes à saisir directement dans le fichier HTML
                'message': '', # message à restituer
                'message_error': 'Erreur de saisie', # message d'erreur à restituer
            },
        )


if __name__ == '__main__':
    
    # Lancement de l'application sans saisir quoique ce soit dans le terminal
    uvicorn.run(app)
