from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount(path='/static/', app=StaticFiles(directory='static'), name='static')

@app.get(
    path='/',
    summary='Default page'
)
def get_home(request: Request):
    return templates.TemplateResponse(
        'indexD002.html',
        {
            'request': request
        }
    )
    
@app.post(
    path='/',
    summary='Retrieve data'
)
async def post_home(request: Request):
    
    # Data retrieved
    form = await request.form()
    
    # Convert data retrieved to dictionary type
    my_dict = dict(form)
    
    for v in my_dict.values():
        print(f"Prénom saisi : {v}")
    
    return templates.TemplateResponse(
        'indexD002.html',
        {
            'request': request
        }
    )

if __name__ == '__main__':
    uvicorn.run(app)
