import os
import urllib.parse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from duckduckgo_search import DDGS

app = FastAPI()

# テンプレートエンジンの設定
templates = Jinja2Templates(directory="app/templates")

# Bangs（ショートカット）の定義
BANGS = {
    "!yt": "https://www.youtube.com/results?search_query=",
    "!gh": "https://github.com/search?q=",
    "!n": "https://www.google.com/search?tbm=nws&q=",
    "!maps": "https://www.google.com/maps/search/",
    "!wiki": "https://ja.wikipedia.org/wiki/",
}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = Form(...)):
    # 1. Bangsのチェック
    for bang, target_url in BANGS.items():
        if q.startswith(f"{bang} "):
            search_term = q[len(bang)+1:].strip()
            return RedirectResponse(url=f"{target_url}{urllib.parse.quote(search_term)}")

    # 2. 通常検索の実行
    results = []
    try:
        with DDGS() as ddgs:
            # 日本地域設定、セーフサーチオフ、最大10件
            ddgs_gen = ddgs.text(q, region="jp-jp", safesearch="off", max_results=10)
            results = [r for r in ddgs_gen]
    except Exception as e:
        print(f"Search Error: {e}")
    
    # 検索結果をテンプレートに渡す
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "results": results, "query": q}
    )

if __name__ == "__main__":
    import uvicorn
    # 環境変数からポートを取得（デフォルトは8000）
    # これによりRender, Koyeb, Railway等での起動失敗を防ぎます
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
