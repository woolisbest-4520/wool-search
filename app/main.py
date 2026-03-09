import os
import urllib.parse
import time
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from duckduckgo_search import DDGS

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Bangsの設定
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
    # 1. Bangs処理
    for bang, target_url in BANGS.items():
        if q.startswith(f"{bang} "):
            search_term = q[len(bang)+1:].strip()
            return RedirectResponse(url=f"{target_url}{urllib.parse.quote(search_term)}")

    # 2. 自動リトライ付き検索ロジック
    results = []
    error_msg = None
    max_retries = 3  # 最大3回リトライ

    for attempt in range(max_retries):
        try:
            with DDGS() as ddgs:
                response = ddgs.text(q, region="jp-jp", safesearch="off", max_results=15)
                results = [r for r in response]
                
                # 結果が取れたらループを抜ける
                if results:
                    break
                
                # 結果が空の場合は、DDG側の準備待ちの可能性があるため少し待機
                time.sleep(1) 
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            error_msg = f"検索エラー: {str(e)}"
            time.sleep(1)  # 失敗時も少し待機

    # 最終的に結果が空だった場合
    if not results and not error_msg:
        error_msg = "検索結果を取得できませんでした。再度お試しください。"
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "results": results, "query": q, "error": error_msg if not results else None}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
