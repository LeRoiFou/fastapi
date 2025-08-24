from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Instanciation du répertoire templates comprenant tous les fichiers HTML
templates = Jinja2Templates(directory='templates')

# Récupération du dossier static comprenant tous les fichiers CSS
app.mount('/static/', StaticFiles(directory='static'), name='static')

@app.get(
    path='/',
    summary="Page par défaut (page 1)"
)
def get_home(request: Request) -> None:
    return templates.TemplateResponse(
        'indexB009.html',
        {'request': request}
    )
    
@app.get(
    path='/page1',
    summary="Accès à la page 1"
)
async def get_page1(request: Request) -> str:
    return templates.TemplateResponse(
        'indexB009_page1.html',
        {'request': request}
    )
    
@app.get(
    path='/page2',
    summary="Accès à la page 2"
)
async def get_page2(request: Request) -> str:
    return templates.TemplateResponse(
        'indexB009_page2.html',
        {'request': request}
    )
    
@app.get(
    path='/page3',
    summary="Accès à la page 3"
)
async def get_page3(request: Request) -> str:
    return templates.TemplateResponse(
        'indexB009_page3.html',
        {'request': request}
    ) 

if __name__ == '__main__':
    uvicorn.run(app)