# 🛍️ CraftOptima — AI Listing Optimizer for Independent Artisans

CraftOptima empowers independent artisans, ceramicists, candle makers, and solo makers on **Etsy, eBay, and Shopify** to out-compete mass-market dropshippers — using open-weight **Google Gemma 4** to generate rank-optimised titles, exactly 13 search tags, 3-tier psychological pricing, sensory artisan copy, and an ElevenLabs audio pitch — without sharing trade secrets with a closed corporate API.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🎯 Algorithmic SEO Title | Platform-aware, keyword-dense title with live character count |
| 🏷️ 13 Search Tags | Exactly 13 tags tuned for Etsy's 13-tag limit or eBay keyword fields |
| 💰 3-Tier Pricing Matrix | Fast-Mover · Artisan Sweet Spot · Premium Gift Box — with rationale |
| 📖 Artisan Origin Story | 80–120 word emotive, sensory-rich craftsmanship narrative |
| 📋 Specifications & Care | 5–7 concise spec bullets + shipping & care tips |
| 🔊 ElevenLabs Audio Pitch | 30-second MP3 voiceover (Sarah voice) for TikTok / Instagram Reels |
| 📦 Product Catalog | Save and revisit all your optimized listings in one place |
| 🌙 Light / Dark Mode | Clean light-blue default theme with one-click dark mode toggle |
| ☁️ Render Deployment | Infrastructure-as-code `render.yaml` for one-click CI/CD |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│           CLIENT (Vercel / Static CDN)                │
│   Vanilla JS · Light-Blue UI · Dark Mode Toggle       │
└──────────┬───────────────────────────┬───────────────┘
           │  Product Input            │  Catalog Sync
           ▼                           ▼
┌──────────────────────────────────────────────────────┐
│                  RENDER BACKEND                       │
│          FastAPI · Python 3.12 · Uvicorn ASGI         │
└────────────┬─────────────────────────┬───────────────┘
             │  Gemma 4 Inference      │  Storage + Voice
             ▼                         ▼
   ┌─────────────────┐       ┌────────────────────────┐
   │  GOOGLE GEMMA 4 │       │  ElevenLabs TTS API    │
   │ gemma-4-26b-a4b │       │  MongoDB Atlas (motor) │
   └─────────────────┘       └────────────────────────┘
```

---

## 🚀 Local Development

### Prerequisites
- Python 3.12+
- A free [Google AI Studio](https://aistudio.google.com) API key (`GEMINI_API_KEY`)
- *(Optional)* [ElevenLabs](https://elevenlabs.io) API key for voice synthesis
- *(Optional)* [MongoDB Atlas](https://www.mongodb.com/atlas) URI for catalog persistence

### 1 — Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:

```env
GEMINI_API_KEY=your_google_ai_studio_key

# Optional — needed for audio pitch feature
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL

# Optional — needed for catalog persistence
MONGODB_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/
MONGODB_DB_NAME=craftoptima_db
```

Then start the server:

```bash
uvicorn main:app --reload --port 8000
```

API docs auto-generated at `http://localhost:8000/docs`.

### 2 — Frontend

Open `frontend/index.html` directly in any browser, **or** serve with VS Code Live Server / Python:

```bash
cd frontend
python -m http.server 3000
# → http://localhost:3000
```

The frontend auto-detects `localhost` and routes API calls to `http://localhost:8000`.

> **Tip:** The catalog requires the backend to be running. Listing generation, tags, pricing, and story all work as soon as `GEMINI_API_KEY` is set.

---

## ☁️ Deployment

### Backend → Render

1. Push this repo to GitHub.
2. Create a new **Web Service** on [render.com](https://render.com) pointing at your repo.
3. Render detects `backend/render.yaml` and configures the service automatically.
4. Add your secret environment variables in the Render dashboard:
   - `GEMINI_API_KEY` *(required)*
   - `ELEVENLABS_API_KEY` *(optional)*
   - `MONGODB_URI` *(optional)*
5. Deploy — the live backend URL becomes your frontend's API target.

### Frontend → Vercel

Drag-and-drop the `frontend/` folder at [vercel.com/new](https://vercel.com/new), or connect via GitHub.  
Update the `API` constant in `frontend/index.html` with your Render backend URL before deploying.

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health, model name, DB status |
| `POST` | `/api/generate-listing` | Gemma 4 full listing generation |
| `POST` | `/api/audio-pitch` | ElevenLabs MP3 voiceover synthesis |
| `POST` | `/api/listings/save` | Save listing to MongoDB Atlas (or in-memory fallback) |
| `GET` | `/api/listings?user_id=…` | Retrieve saved listings for a given user |

Full interactive docs available at `GET /docs` (Swagger UI).

### Example: Generate a Listing

```bash
curl -X POST http://localhost:8000/api/generate-listing \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Handmade Ceramic Matcha Bowl",
    "materials": "Stoneware clay, food-safe glaze",
    "target_platform": "Etsy",
    "target_audience": "Tea ceremony enthusiasts",
    "key_features": "Wheel-thrown, 14oz, includes bamboo whisk",
    "current_price_estimate": 22.00
  }'
```

---

## 💡 Why Open-Weight Gemma

| Concern | Closed Proprietary AI | Open-Weight Gemma in CraftOptima |
|---|---|---|
| **Merchant IP Privacy** | Product blueprints transmitted to corporate training servers | Zero data exfiltration — can run fully on-device or private VMs |
| **Unit Economics** | Per-token fees erode slim side-hustle margins | Predictable hosting cost; free on local hardware via Ollama |
| **Vendor Lock-in** | Sudden deprecations or price hikes break your tool | Open weights cannot be retroactively revoked or price-hiked |
| **Schema Compliance** | Prone to prompt drift | Gemma 4 + `response_mime_type="application/json"` enforces strict output |

---

## 📄 License

[MIT](./LICENSE) — open source, built for creator empowerment.
