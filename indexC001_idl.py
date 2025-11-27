from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

from treatments.indexC001_treatments import department, city, prefix

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount(path='/static/', app=StaticFiles(directory='static'), name='static')

@app.get(
    path='/',
    summary='Default page',
)
def get_home(request: Request):
    
    year_list = ['2023', '2024', '2025']
    
    category_list = ['ATE1', 'ATE2', 'ATE3', 'BUR1', 'BUR2', 'BUR3', 'CLI1',
                     'CLI2', 'CLI3', 'CLI4', 'DEP1', 'DEP2', 'DEP3', 'DEP4', 
                     'DEP5', 'ENS1', 'ENS2', 'EXC1', 'HOT1', 'HOT2', 'HOT3',
                     'HOT4', 'HOT5', 'IND1', 'IND2', 'MAG1', 'MAG2', 'MAG3', 
                     'MAG4', 'MAG5', 'MAG6', 'MAG7', 'SPE1', 'SPE2', 'SPE3',
                     'SPE4', 'SPE5', 'SPE6', 'SPE7',]

    department_list = department()
    
    return templates.TemplateResponse(
        'indexC001_idl.html',
        {
            'request': request,
            'year_list': year_list,
            'category_list': category_list,
            'department_list': department_list,
        }
    )
    
@app.post(
    path='/area',
    summary='Determination of the weighted area'
)
async def post_area(request: Request):
    
    form = await request.form()
    my_dict = dict(form)
    
    areaP1 = int((my_dict['P1']))
    areaP2 = int(my_dict['P2'])
    areaP3 = int(my_dict['P3'])
    areaPK1 = int(my_dict['PK1'])
    areaPK2 = int(my_dict['PK2'])
    area_sum = areaP1 + areaP2 + areaP3 + areaPK1 + areaPK2
    
    p1 = areaP1 * 1.00
    p2 = areaP2 * 0.50
    p3 = areaP3 * 0.20
    pk1 = areaPK1 * 0.50
    pk2 = areaPK2 * 0.20
    area_weighted_sum = p1 + p2 + p3 + pk1 + pk2
    
    return templates.TemplateResponse(
        'indexC001_idl.html',
        {'request': request,
         'areaP1': areaP1,
         'areaP2': areaP2,
         'areaP3': areaP3,
         'areaPK1': areaPK1,
         'areaPK2': areaPK2,
         'area_sum': area_sum,
         'p1': p1,
         'p2': p2,
         'p3': p3,
         'pk1': pk1,
         'pk2': pk2,
         'area_weighted_sum': area_weighted_sum,
         }
    )
    
@app.post(
    path='/city',
    summary='Retrieve the selected city'
    )
async def post_city(department: str=Form(...),):
    
    # Récupération la fonction city()
    city_list = city(str(department[0:2]))

    return JSONResponse({"city_list": city_list})


if __name__ == '__main__':
    uvicorn.run(app)
