from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os
import pickle
import uuid
import time
import uvicorn

from treatments.indexB008_treatments import treatments

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Instanciation du répertoire et des fichiers HTML
templates = Jinja2Templates(directory='templates')

# Récupération du fichier static et de ses fichiers CSS
app.mount('/static/', StaticFiles(directory='static'),name='static')

# Chemin absolu du dossier où se trouve ce script (c:\Users\LRCOM\Documents\...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ajout du répertoire data (...\Python\fastapi_test\app\data)
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Création du dossier 'data' s'il n'existe pas
os.makedirs(DATA_DIR, exist_ok=True)

# 1ère page HTML : page par défaut
@app.get('/',
         response_class=HTMLResponse,
         summary="Page @ par défaut",
         description="""
         Page affichant le fichier à récupérer et à charger le fichier Excel sélectionné
         """,
         )
def get_home(request: Request):
    return templates.TemplateResponse(
        'indexB008_home.html', # fichier HTML lié
        {"request": request} # requêtes possibles directement sur le fichier HTML
    )

# 2ème page HTML : Affecter un titre à chaque civilité... sauf si erreur...
@app.post('/upload',
          response_class=HTMLResponse,
          summary='Table des civilités et des titres à affecter',
          description="""
          Page affichant une table comprenant les civilités et les titres à affecter
          
          arg import_file: chargement des données du fichier Excel
          """,
          )
async def post_upload(
    request: Request,
    import_file: UploadFile=File(...),
) -> None:
    
    # Assignation d'un nom du fichier chargé et de son extension
    filename = import_file.filename
    
    # Vérification que le fichier chargé a une extension .xlsx
    if not filename.lower().endswith('.xlsx'):
        return templates.TemplateResponse(
            'indexB008_error.html', # fichier HMTL lié
            {'request': request, # requêtes à effectuer sur le fichier HTML
             'message': "❌ Le fichier doit être au format .xlsx (Excel).",
             }
        )
    
    # Instruction asynchrone ci-après permettant de lire le fichier Excel en 
    # mémoire (en mode binaire) sans bloquer l'application
    contents = await import_file.read()
    
    # Assignation d'un nom de fichier temporaire Excel
    input_path = 'temp_upload.xlsx'
    
    try:
        # Sauvegarde temporaire pour que les traitements polars
        # s'opérent sur ce fichier
        with open(input_path, 'wb') as f:
            f.write(contents)
            
        # Récupération de la méthode treatments()
        # sur les traitements effectués sur la DF
        civilities = treatments(input_path)
        
        # Suppression du fichier temporaire
        os.remove(input_path)
        
        # Assignation d'une liste de titres
        titles = ['Maître', 'Seigneur', 'Esclave']
        
        return templates.TemplateResponse(
            'indexB008_formulaire.html', # fichier HTML lié
            {'request': request, # requêtes à effectuer sur le fichier HTML
             'civilites': civilities, # Colonne des civilités
             'titres': titles, # Colonne des titres
             }
            )
    
    # Fichier invalide...
    except ValueError:
        return templates.TemplateResponse(
            'indexB008_error.html', # fichier HTML lié
            {'request': request, # requêtes à effectuer sur le fichier HTML
             'message': "❌ Le fichier chargé n'est pas un fichier Excel valide. Veuillez réessayer..."
             }
        )
    
    # Erreur inattendue...
    except Exception as e:
        return templates.TemplateResponse(
            'indexB008_error.html', # fichier HTML lié
            {'request': request, # requêtes à effectuer sur le fichier HTML
             'message': f"❌ Une erreur est survenue : {str(e)}"
             }
        )

# 3ème page HTML : Résultats des affectations
@app.post("/submit",
          response_class=HTMLResponse,
          summary="Affichage et téléchargement des titres affectés aux civilités",
          description="""
          Page affichant les titres affectés aux civilités + téléchargement des données sous format pickle
          """,)
async def post_submit(request: Request):
    
    # Récupération de la table avec les civilités et les titres rattachés
    form = await request.form()
    
    # Conversion en type dictionnaire
    results = dict(form)

    # Création d'un identifiant unique sous la forme de caractères sous la forme :
    # 0c6b9a1e-f85b-42a6-bec7-b6cf37934cb0 -> impossible d'avoir 2 fois le même
    unique_id = str(uuid.uuid4())
    
    # Assignation du nom de fichier avec la concaténation de l'identifiant ci-avant
    filename = f"civilite_titres_{unique_id}.pickle"
    
    # Assignation du chemin complet du fichier pickle (répertoires + nom du fichier)
    filepath = os.path.join(DATA_DIR, filename)
    
    # 🔁 Nettoyage automatique : suppression des fichiers .pickle 
    # de plus d'1 heure
    now = time.time()
    expiration_seconds = 3600  # 1 heure
    
    # Pour chaque fichier dans le répertoire ciblé (/data)...
    for f in os.listdir(DATA_DIR):
        
        # Si le nom du fichier a pour terminaison .pickle...
        if f.endswith(".pickle"):
            
            # Assignation du chemin complet du fichier pickle 
            # (répertoires + nom du fichier)
            full_path = os.path.join(DATA_DIR, f)
            
            try:
                # Si le fichier téléchargé a un temps expiré...
                if now - os.path.getmtime(full_path) > expiration_seconds:
                    
                    # Suppression du fichier .pickle
                    os.remove(full_path)
                    
            except Exception as e:
                print(f"Erreur lors de la suppression de {f} : {e}")  # log utile

    # Chargement des titres affectés aux civilités dans un fichier pickle
    with open(filepath, "wb") as f:
        pickle.dump(results, f)

    return templates.TemplateResponse(
        "indexB008_results.html",
        {
            "request": request,
            "results": results,
            "download_link": f"/download/{filename}",
        }
    )

# 4ème page HTML : téléchargements 
@app.get('/download/{filename}')
def download_pickle(filename: str):
    file_path = os.path.join(DATA_DIR, filename)

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            media_type='application/octet-stream',
            filename=filename
        )
    return HTMLResponse("❌ Fichier introuvable", status_code=404)

if __name__ == '__main__':
    uvicorn.run(app)
