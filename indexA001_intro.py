"""
Premier essai avec la librairie fastapi

Dans ce script, on a utilisé 4 fichiers :
- Le fichier indexA001_intro.py qui permet de lancer l'application
- Le fichier indexA001_treatments.py dans le répertoire app_metier qui permet 
de recourir à la modularité
- Le fichier indexA001.html dans le répertoire templates qui permet d'afficher les 
données de l'application
- Le fichier indexA001_style.css.css dans le répertoire static qui permet de 
mettre en forme les données de l'application

Les librairies suivantes ont été importées :
- FastApi : créer l'application web
- Form : récupérer les données envoyées par un formulaire HTML
- Request : requête HTTP (nécessaire pour utiliser des templates)
- HMLResponse : spécifie que la route retourne du HTML (utile pour les navigateurs)
- Jinja2Templates permet d'utiliser des fichiers HTML comme modèles (index.html), 
avec des variables dynamiques (comme {{ result }})
- StaticFiles sert à rendre accessibles des fichiers statiques (CSS, JS, images…)
- uvicorn qui permet de lancer l'appli sans saisir quoique ce soit dans le terminal

Date : 04/06/2025
Editeur : Laurent REYNAUD
"""

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# Récupération de la fonction operation_complexe() dans le répertoire treatments
from treatments.indexA001_treatments import operation_complexe

# Instanciation de la sous-librairie FastApi
app = FastAPI()

# Indique à FastAPI d’aller chercher les fichiers .html dans le dossier templates/.
# instancié dans une variable
templates = Jinja2Templates(directory="templates")

# Permet d'accéder aux fichiers du dossier static/ via l’URL /static/
app.mount("/static/", StaticFiles(directory="static"), name="static")

@app.get("/", # URL d'accès
         response_class=HTMLResponse, # Affichage en HTML
         summary="Accès à la page par défaut",
         description="""
         Retour de la page web par défaut sous format HTML
         
         param: requête par défaut en cas de chargement HTML sinon erreur
         """,
         )
async def home(request: Request):

    # Accès à la page HTML
    return templates.TemplateResponse(
        "indexA001.html", 
        {"request": request, "result": ""}) # "result" vide ici car 1ère visite

@app.post("/", # URL d'accès
          response_class=HTMLResponse, # Affichage en HTML
          summary="Modification de la page suite intervention de l'utilisateur",
          description="""
          Retour de la page sous format HTML suite intevention de l'utilisateur
          
          param: requête par défaut en cas de chargement HTML sinon erreur
          args: nombre entier saisi par l'utilisateur dans le composant ciblé
          """,
          )
async def calculer(request: Request, valeur: int = Form(...)) -> str:
    
    # Récupération de la fonction operation_complexe avec en argument le nombre
    # entier saisir par l'utilisateur
    resultat = operation_complexe(valeur)
    
    return templates.TemplateResponse(
        "indexA001.html", 
        {"request": request, "result": f"{resultat}" # result" : résultat à obtenir
    })

if __name__ == '__main__':
    uvicorn.run(app)
