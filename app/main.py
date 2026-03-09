import os
import urllib.parse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from duckduckgo_search import DDGS

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

BANGS = {
    "!yt": "https://www.youtube.com/results?search_query=",
    "!gh": "https://github.com/search?q=",
}

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = Form(...)):
    # 1. Bangs処理
    for bang, target_url in BANGS.items():
        if q.startswith(f"{bang} "):
            search_term = q[len(bang)+1:].strip()
            return RedirectResponse(url=f"{target_url}{urllib.parse.quote(search_term)}")

    # 2. 検索実行
    results = []
    error_msg = None
    try:
        with DDGS() as ddgs:
            # 最新の ddgs.text は list() で囲うか、ループで回す必要があります
            search_results = ddgs.text(
                q, 
                region="jp-jp", 
                safesearch="off", 
                max_results=10
            )
            # ジェネレータからリストに変換
            results = [r for r in search_results]
            
            # デバッグ用：サーバーのコンソールに件数を表示
            print(f"Query: {q}, Found: {len(results)} results")
            
    except Exception as e:
        error_msg = f"Search Error: {str(e)}"
        print(error_msg)
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "results": results, "query": q, "error": error_msg}
    )
