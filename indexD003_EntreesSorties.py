from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount(path='/static/', app=StaticFiles(directory='static'), name='static')

def get_fruits_dic():
    return {
        'Fruits': ['Kiwi', 'Banane', 'Noix de coco', 'Ananas'],
        'Prix au Kg (en €)': [3.10, 1.60, 1.00, 1.20]
    }
    

@app.get(
    path='/',
    summary='Page default'
)
def get_home(request: Request):
    
    return templates.TemplateResponse(
        'indexD003.html',
        {
            'fruits': get_fruits_dic(),
            'request': request
        }
    )
    

@app.post(
    path='/',
    summary='Retrieve data'
)
async def post_home(request: Request):
    
    # HMTL data retrieved
    form = await request.form()
    # Data convert to dict type
    result_dict = dict(form)
    # Fruit and price retrieved
    fruit_selected = list(result_dict.items())[0][1]
    quantity_selected = int(list(result_dict.values())[1])
    
    # Dictionnary retrieved
    fruits_dict = get_fruits_dic()
    # Index value
    index = fruits_dict['Fruits'].index(fruit_selected)
    # Price retrieved
    price = fruits_dict['Prix au Kg (en €)'][index]
    
    # For HTML file
    total_result = int(quantity_selected * price)
    
    
    return templates.TemplateResponse(
        'indexD003.html',
        {   
            'fruits': fruits_dict,
            'request': request,
            'fruit_selected': fruit_selected,
            'quantity_selected': quantity_selected,
            'price': price,
            'result': total_result,
        }
    )

if __name__ == '__main__':
    uvicorn.run(app)
