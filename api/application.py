from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import pandas as pd

app = FastAPI()

templates = Jinja2Templates(directory="templates")

iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

@app.get("/")
def read_root():
    return {"Status": "200 (OK)", "Message": "API deployed successfully!"}

@app.get("/data", response_class=HTMLResponse)
def get_data(request: Request):
    return templates.TemplateResponse(name="table.html", context={"request": request, 'table': iris.to_html()})
