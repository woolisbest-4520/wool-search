import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from duckduckgo_search import DDGS

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = Form(...)):
    results = []
    try:
        with DDGS() as ddgs:
            # 検索実行 (日本地域、安全検索オフ、10件)
            ddgs_gen = ddgs.text(q, region="jp-jp", safesearch="off", max_results=10)
            results = [r for r in ddgs_gen]
    except Exception as e:
        print(f"Error: {e}")
    
    return templates.TemplateResponse("index.html", {"request": request, "results": results, "query": q})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
