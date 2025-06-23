from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os
from treatments.indexB007_treatments import treatments

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Instanciation du répertoire templates comprenant tous les fichiers HTML
templates = Jinja2Templates(directory='templates')

# Récupération du dossier static comprenant tous les fichiers CSS
app.mount('/static/', StaticFiles(directory='static'), name='static')

@app.get('/', # URL page par défaut
         response_class = HTMLResponse, # affichage en page HTML
         summary = 'Page par défaut',
         description="""
         Retour de la page par défaut
         
         param request: requête à saisir directement sur le fichier HTML
         """,
         )
async def get_home(request: Request):
    return templates.TemplateResponse(
        'indexB007_upload.html', # Fichier HTML pour la page @ par défaut
        {'request': request} # requêtes à saisir directement sur le fichier HTML
    )

@app.post("/upload", # URL pour affecter un titre à chaque civilité
          response_class=HTMLResponse, # affichage en HTML
          summary="Chargement du fichier Excel : titres à affecter",
          description="""
          Retour en table les données du fichier Excel chargé avec les titres à rattacher
          
          param request: requêtes à opérer directement sur le fichier HTML
          args import_file: chargement des données du fichier Excel
          """,)
async def upload_excel(
    request: Request, 
    import_file: UploadFile = File(...),
    ) -> None:
    
    # Assignation du nom du fichier chargé et de son extension
    filename = import_file.filename
    
    # Vérification que le fichier chargé a une extension .xlsx
    if not filename.lower().endswith(".xlsx"):
        return templates.TemplateResponse(
            "error.html", # Affichage de la page HTML
            {"request": request, # Requêtes à effectuer sur le fichier HTML
             "message": "❌ Le fichier doit être au format .xlsx (Excel)."}
        )
    
    # Instruction asynchrone ci-après permettant de lire le fichier Excel en mémoire
    # (en mode binaire) sans bloquer l'application (instruction await)
    contents = await import_file.read()

    # Assignation d'un nom de fichier temporaire Excel
    input_path = "temp_upload.xlsx"
    
    try:
        # Sauvegarde temporaire pour que les traitements polars
        # s'opèrent sur ce fichier
        with open(input_path, "wb") as f:
            f.write(contents)

        # Récupération de la méthode treatments() 
        # sur les traitements effectués sur la DF
        civilities = treatments(input_path)

        # Supprimer le fichier temporaire
        os.remove(input_path)
        
        # Assignation d'une liste de titres
        titles = ['Seigneur', 'Maître', 'Esclave']

        return templates.TemplateResponse("indexB007_formulaire.html", {
            "request": request,
            "civilites": civilities,
            "titres": titles,
        })
    
    # Fichier invalide...
    except ValueError:
        
        return templates.TemplateResponse(
            "indexB007_error.html", # Affichage de la page HTML
            {"request": request, # Requêtes à effectuer sur le fichier HTML
             "message": "❌ Le fichier chargé n'est pas un fichier Excel valide. Veuillez réessayer."}
        )
    
    # Erreur inattendue...
    except Exception as e:
        
        return templates.TemplateResponse(
            "indexB007_error.html", # Affichage de la page HTML
            {"request": request, # Requêtes à effectuer sur le fichier HTML
             "message": f"❌ Une erreur est survenue : {str(e)}"}
        )
        
@app.post("/submit", # URL résultat des affectations
          response_class=HTMLResponse, # affichage en HTML
          summary="Titres rattachés aux civilités",
          description="""
          Retour des titres rattachés aux civilités
          
          param request: requêtes à effectuer sur le fichier HTML
          """,
          )
async def submit(request: Request):
    
    # Récupération de la table avec les civilités et les titres rattachés
    form = await request.form()
    
    # Conversion en type dictionnaire
    results = dict(form)
    
    return templates.TemplateResponse("indexB007_resultats.html", {
        "request": request,
        "results": results
    })

if __name__ == '__main__':
    
    # Lancement direct de l'applications sans rien saisir dans le terminal
    uvicorn.run(app)
