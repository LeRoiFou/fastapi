"""
Lien n° 1 : https://www.youtube.com/watch?v=maCSBgFHoZ4
Introduction à la librairie FastApi

Lien n° 2 : https://www.youtube.com/watch?v=otkuRlCwtGc&list=PL9DK-47Rpfjjtk7mBH6AyZSHhJYXSXUn7&index=2
Documentation de l'API : saisir sur la page web -> /docs 

A saisir dans le terminal:
uvicorn indexA002_intro:app --reload

Date : 04/06/2025
"""

from fastapi import FastAPI

# Instanciation de la sous-librairie FastApi
app = FastAPI()

# Route GET – Affiche la page
# @app.get("/test") : définit une route accessible via le navigateur 
@app.get('/test')
async def test():
    
    # Message à afficher
    return {"Message": "Test ok !"}
