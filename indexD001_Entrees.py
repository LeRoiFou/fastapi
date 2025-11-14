from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount(path='/static/', app=StaticFiles(directory='static'), name='static')

@app.get(
    path='/',
    summary='',
    description=""
)
def get_home(request: Request):
    
    my_dict = {'Nom': ['Gerald', 'White', 'Gallagher', 'Bohl',], 
               'Prenom': ['John', 'Walter', 'Franck', 'Kevin',],
               'Age': [48, 55, 60, 30],
               }
    
    return templates.TemplateResponse(
        'indexD001.html',
        {   
            'request': request,
            'message': 'Hello world!',
            'dict': my_dict,
        }
    )

if __name__ == '__main__':
    uvicorn.run(app)
