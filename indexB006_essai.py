from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from treatments import indexB006_treatments as my_func

# Instanciation de la sous-librairie
app = FastAPI()

# Récupération des fichiers HTML contenus dans le répertoire templates
templates = Jinja2Templates(directory="templates")

# Récupération des fichiers CSS contenus dans le répertoire static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Création d'un répertoire 'temp' s'il n'existe pas et assignation d'une constante :
# fichier Excel à télécharger
os.makedirs("output", exist_ok=True)
OUTPUT_PATH = "output/resultat.xlsx"

@app.get("/", # page URL par défaut
         response_class=HTMLResponse, # affichage sous format HTML
         summary="Page par défaut",
         description="""
         Retour page par défaut
         
         param request: requêtes à effectuer directement sur le fichier HTML
         """
         )
def form_page(request: Request) -> None:
    return templates.TemplateResponse(
        "indexB006.html", # Affichage de la page HTML
        {"request": request} # Requêtes à effectuer sur le fichier HTML
        )

@app.post("/process", # page URL pour la saisie des données (POST)
          response_class=HTMLResponse, # affichage sous format HTML
          summary="Traitements opérés sur le fichier Excel chargé",
          description="""
          Retour du fichier Excel traité (sous-librairie FileResponse) à télécharger
          
          param request: requêtes à effectuer directement sur le fichier HTML
          arg import_file: fichier Excel chargé
          arg cr1: nombre entier à saisir (salaires exclus fourchette bas)
          arg cr2: nombre entier à saisir (salaires exclus fourchette haut)
          arg cr3: str à sélectionner dans le menu déroulant (civilité)
          """,
          )
async def process_file(
    request: Request,
    import_file: UploadFile = File(...),
    cr1: int = Form(...),
    cr2: int = Form(...),
    cr3: str = Form(...)
) -> None:
    
    # Assignation du nom du fichier chargé et de son extension
    filename = import_file.filename
    
    # Vérification que le fichier chargé a une extension .xlsx
    if not filename.lower().endswith(".xlsx"):
        return templates.TemplateResponse(
            "indexB006_error.html", # Affichage de la page HTML
            {"request": request, # Requêtes à effectuer sur le fichier HTML
             "message": "❌ Le fichier doit être au format .xlsx (Excel)."}
        )
    
    # Instruction asynchrone ci-après permettant de lire le fichier Excel en mémoire
    # (en mode binaire) sans bloquer l'application (instruction await)
    contents = await import_file.read()
    
    # Assignation d'un nom de fichier temporaire Excel
    input_path = "temp_upload.xlsx"
    
    try:
        # Sauvegarde temporaire pour que les traitements pandas s'opèrent sur ce fichier
        with open(input_path, "wb") as f:
            f.write(contents)

        # Traitement du fichier Excel lu à partir de la fonction treatments du
        # fichier indexB006_treatments.py en convertissant les bytes 
        my_func.treatments(input_path, cr1, cr2, cr3, OUTPUT_PATH)

        # Suppression du fichier temporaire servi de base pour les traitements pandas
        os.remove(input_path)

        # Affiche la page de confirmation
        return templates.TemplateResponse(
            "indexB006_confirmation.html", # Affichage de la page HTML
            {"request": request} # Requêtes à effectuer sur le fichier HTML
            )
    
    # Fichier invalide
    except ValueError:
        
        return templates.TemplateResponse(
            "indexB006_error.html", # Affichage de la page HTML
            {"request": request, # Requêtes à effectuer sur le fichier HTML
             "message": "❌ Le fichier chargé n'est pas un fichier Excel valide. Veuillez réessayer."}
        )
    
    #Erreur inattendue   
    except Exception as e:
        
        return templates.TemplateResponse(
            "indexB006_error.html", # Affichage de la page HTML
            {"request": request, # Requêtes à effectuer sur le fichier HTML
             "message": f"❌ Une erreur est survenue : {str(e)}"}
        )

@app.get("/download", # page URL pour le chargement du fichier Excel traité (GET)
         response_class=HTMLResponse, # affichage sous format HTML
         summary="Téléchargement du fichier Excel traité",
         description="Retour du fichier Excel traité",
         )
async def download_file():
    return FileResponse(
        path=OUTPUT_PATH,
        filename="resultat.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
if __name__ == '__main__':
    # Lancement du serveur local sans rien saisir dans le terminal
    uvicorn.run(app)
