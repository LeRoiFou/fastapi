from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Tuple
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount(path='/static/', app=StaticFiles(directory='static'), name='static')

# Constant: VAT rate
VAT_RATES = {
    'normal': 0.20,
    'intermediary': 0.10,
    'reduced': 0.055,
    'super-reduced': 0.021
}

def vat_calculate(amount: float, base: str, rate:str) -> Tuple[float, float, float]:
    """
    VAT calculator function
    
    :param amount: amount entered
    :type amount: float
    :param base: base entered
    :type base: str
    :param rate: rate entered
    :type rate: str
    :return: Result of the base price excluding VAT, VAT and total price including VAT
    :rtype: Tuple[float, float, float]
    """
    
    # Default values
    line1 = 0
    line2 = 0
    line3 = 0
    
    # Conditions
    if base == 'TTC':
        line1 = amount / (1 + VAT_RATES[rate])
        line2 = amount / (1 + VAT_RATES[rate]) * VAT_RATES[rate]
        line3 = amount
    elif base == 'HT':
        line1 = amount
        line2 = amount * VAT_RATES[rate]
        line3 = amount * (1 + VAT_RATES[rate])
    elif base == 'TVA':
        line1 = amount / VAT_RATES[rate]
        line2 = amount
        line3 = amount / VAT_RATES[rate] * (1 + VAT_RATES[rate])
    
    return line1, line2, line3

@app.get(
    path='/',
    summary='Page default'
)
def get_home(request: Request):
    return templates.TemplateResponse(
        'indexD004.html',
        {
            'request': request
        }
    )
    
@app.post(
    path='/',
    summary='Data retrieved'
)
async def post_home(request: Request):
    
    # Data retrieved
    my_dict = dict(await request.form())
    
    # Amount entered
    amount = float(my_dict.get('amount'))

    # Base selected
    base = my_dict.get('base')
    
    # Rate selected
    rate = my_dict.get('rate')
    
    # vat_calculate() function called
    line1, line2, line3 = vat_calculate(amount, base, rate)
    
    return templates.TemplateResponse(
        'indexD004.html',
        {
            'request': request,
            'line1': round(line1, 2),
            'line2': round(line2, 2),
            'line3': round(line3, 2),
        }
    )

if __name__ == '__main__':
    uvicorn.run(app)
