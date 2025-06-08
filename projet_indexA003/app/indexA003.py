"""
Préalablement mettre le dossier dans Github

Dans le terminal aller dans le répertoire 'projet' puis saisir dans le terminal :
docker compose --project-name projet up -d
"""

from fastapi import FastAPI
import uvicorn

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Route GET : accès à la page
@app.get('/') # URL
async def read_route():
    return {'Message': 'Hello World!'}

if __name__ == '__main__' :
    
    # Lancement direct de l'application sans saisir quoique ce soit dans le terminal
    uvicorn.run(app)
