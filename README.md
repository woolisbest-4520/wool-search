# 🐑 Wool-Search (Beta)
**Wool-Search** は、プライバシーを極限まで重視した、オープンソースの超軽量・高速メタ検索エンジンです。
DuckDuckGoの検索エンジンをコアに、ログを一切残さず、誰でも1クリックで「自分専用の検索窓」を全世界にデプロイできることを目的に開発されました。



---

## 🚀 1-Click Deployment
お好きなプラットフォームを選んで、今すぐ自分専用の検索エンジンを立ち上げましょう。

### **主要 PaaS (Recommended)**
| Service | Deploy Status |
| :--- | :--- |
| **Render** | [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/woolisbest-4520/wool-search) |
| **Railway** | [![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/deploy?repo=https://github.com/woolisbest-4520/wool-search) |
| **Vercel** | [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/woolisbest-4520/wool-search) |
| **Koyeb** | [![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/woolisbest-4520/wool-search) |

### **開発・AI・サンドボックス環境**
| Platform | Link |
| :--- | :--- |
| **Hugging Face** | [🤗 Create Space](https://huggingface.co/new-space?template=woolisbest-4520/wool-search) |
| **CodeSandbox** | [🧪 Open in CodeSandbox](https://codesandbox.io/s/github/woolisbest-4520/wool-search) |
| **Glitch** | [🎏 Remix on Glitch](https://glitch.com/edit/#!/import/github/woolisbest-4520/wool-search) |
| **Replit** | [🌀 Import on Replit](https://replit.com/github/woolisbest-4520/wool-search) |

---

## ✨ Wool-Search の特徴
- **完全匿名性**: サーバーサイドでクエリを処理し、クライアントのIPアドレスやUser-Agentを検索エンジンに渡しません。
- **超高速・軽量**: 依存関係を最小限に抑えた Python + FastAPI 構成。
- **Bangs機能**: 検索ワードの先頭に `!yt` や `!gh` をつけるだけで、目的のサイトへダイレクトジャンプ。
- **レスポンシブUI**: Tailwind CSS を採用し、PC・スマホの両方で快適に動作。
- **どこでもデプロイ**: `render.yaml`, `fly.toml`, `vercel.json` など、あらゆる設定ファイルを同梱。

---

## 🛠 ローカルセットアップ

### **1. Docker で起動 (推奨)**
```bash
git clone [https://github.com/woolisbest-4520/wool-search.git](https://github.com/woolisbest-4520/wool-search.git)
cd wool-search
docker-compose up -d
