from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

from treatments.indexB007_treatments import treatments as my_func

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount(path='/static/', app=StaticFiles(directory='static'), name='static')

@app.get(
    path='/',
    summary='',
    description=""""""
)
def get_home(request: Request) -> None:
    """
    """
    return templates.TemplateResponse(
        'index_test.html',
        {'request': request}
    )
    
@app.post(
    path='/process',
    summary='',
    description=""""""
)
async def post_process(
    request: Request,
    upload: UploadFile=File(...)
    ) -> str:
    """
    """
    
    contents = await upload.read()
    temp_file = 'temp_file.xlsx'
    with open(temp_file, 'wb') as f:
        f.write(contents)
        
    civilities = my_func(temp_file)
    os.remove(temp_file)
    
    title = ['Seigneur', 'Maître', 'Esclave']
    
    return templates.TemplateResponse(
        'index_test2.html',
        {'request': request,
         'civilities': civilities,
         'title': title
         }
    )
    
@app.post(
    path='/result',
    summary='',
    description=""""""
)
async def post_result(request: Request):
    """
    """
    
    result = await request.form()
    
    return templates.TemplateResponse(
        'index_test3.html',
        {'request': request,
         'result': result
         }
    )
    
    

if __name__ == '__main__':
    uvicorn.run(app)
