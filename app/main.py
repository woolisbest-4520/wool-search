import os
import urllib.parse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from duckduckgo_search import DDGS

app = FastAPI()

# テンプレート設定
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
    return templates.TemplateResponse("index.html", {"request": request, "results": None, "query": ""})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = Form(...)):
    # 1. Bangs（ショートカット）の処理
    for bang, target_url in BANGS.items():
        if q.startswith(f"{bang} "):
            search_term = q[len(bang)+1:].strip()
            return RedirectResponse(url=f"{target_url}{urllib.parse.quote(search_term)}")

    # 2. DuckDuckGo 検索の実行
    results = []
    error_msg = None
    try:
        with DDGS() as ddgs:
            # 日本地域(jp-jp), セーフサーチオフ
            response = ddgs.text(q, region="jp-jp", safesearch="off", max_results=15)
            # ジェネレータをリストに変換（重要）
            results = [r for r in response]
            
            if not results:
                print(f"No results found for query: {q}")
    except Exception as e:
        error_msg = f"検索エラーが発生しました: {str(e)}"
        print(error_msg)
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "results": results, "query": q, "error": error_msg}
    )

if __name__ == "__main__":
    import uvicorn
    # PaaS(Render/Koyeb等)のポート割り当てに対応
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
