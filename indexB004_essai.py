from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Accès aux fichiers HTML du répertoire templates
templates = Jinja2Templates(directory='templates')

# Accès au répertoire static contenant les fichiers CSS
app.mount('/static/', StaticFiles(directory='static'), name='static')

@app.get('/hello', # URL avec chemin spécifié
         response_class=HTMLResponse, # affichage en HTML
         summary="Page HTML à afficher par défaut",
         description="""
         Retour de la page HTML par défaut
         
         param request: à mentionner sinon erreur
         """,
         )
async def get_hello(request: Request):
    return templates.TemplateResponse(
        'indexB004.html', # accès au fichier HTML
        { # Données à restituer
            'request': request, # obligatoire pour une restitution en HTML
            'message': '', # message de réponse
            'error_message': '', # message d'erreur
        },
    )

@app.post('/hello', # URL avec chemin spécifié
          response_class=HTMLResponse, # affichage en HTML
          summary="Page HTML avec restitution des données saisies",
          description="""
          Retour de la page HTML avec données saisies par l'utilisateur
          
          param request: à mentionner sinon erreur
          args message: données saisies par l'utilisateur de type str !!!
         """,
          )
async def post_hello(request: Request, message: str = Form(...)) -> str:  
    # La restitution est un entier
    try:
        # Conversion du message saisi de type str en type int
        int_message = int(message)
        
        return templates.TemplateResponse(
            'indexB004.html', # accès au fichier HTML
            { # Données à restituer
                'request': request, # obligatoire pour une restitution en HTML
                'message': int_message, # message de réponse
                'error_message': '', # message d'erreur
            },
        )
        
    # Erreur si la restitution n'est pas un entier
    except ValueError:
        return templates.TemplateResponse(
            'indexB004.html', # accès au fichier HTML
            { # Données à restituer
                'request': request, # obligatoire pour une restitution en HTML
                'message': '', # message de réponse
                'error_message': 
                    'Veuillez entrer un nombre entier valide !', # message d'erreur
            },
        )

if __name__ == '__main__':
    # Lancement du serveur local
    uvicorn.run(app)
