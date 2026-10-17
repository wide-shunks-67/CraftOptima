# 🛍️ CraftOptima — Open-Weight AI Listing Optimizer for Artisan Side-Hustles

> **Hacktoberfest 2026 · Week 2 · "Side Hustle"** — Build something with open-source AI that someone would actually pay for.

CraftOptima empowers independent artisans, ceramicists, candle makers, and solo makers on **Etsy, eBay, and Shopify** to out-compete mass-market dropshippers — using open-weight **Google Gemma 4** to generate rank-optimised titles, exactly 13 search tags, 3-tier psychological pricing, sensory artisan copy, and an ElevenLabs audio pitch — all without sharing trade secrets with a closed corporate API.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🎯 Algorithmic SEO Title | Platform-aware, keyword-dense title with character count |
| 🏷️ 13 Search Tags | Exactly 13 tags tuned for Etsy's 13-tag limit or eBay keyword fields |
| 💰 3-Tier Pricing Matrix | Fast-Mover · Artisan Sweet Spot · Premium Gift Box Edition |
| 📖 Origin Story | 80–120 word emotive, sensory-rich craftsmanship narrative |
| 🔊 ElevenLabs Audio Pitch | 30-second MP3 voiceover for TikTok / Instagram Reels |
| 🔒 Private Seller Catalog | Device-isolated MongoDB Atlas catalog, zero sign-up needed |
| ☁️ Render Deployment | Infrastructure-as-code `render.yaml` for one-click CI/CD |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│           CLIENT (Vercel / Static CDN)                │
│   Tailwind CSS + Vanilla JS · Dark-mode Glassmorphism │
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
- A free [Google AI Studio](https://aistudio.google.com) API key
- *(Optional)* ElevenLabs API key & MongoDB Atlas URI

### 1 — Backend

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

# Create your environment file
cp .env.example .env
# Then open .env and fill in GEMINI_API_KEY (required)
# ELEVENLABS_API_KEY and MONGODB_URI are optional for local testing

uvicorn main:app --reload --port 8000
```

API docs auto-generated at `http://localhost:8000/docs`.

### 2 — Frontend

Open `frontend/index.html` directly in any browser, **or** serve with:

```bash
cd frontend
python -m http.server 3000
# → http://localhost:3000
```

The frontend auto-detects `localhost` and points requests to `http://localhost:8000`.

---

## ☁️ Render Deployment

1. Push this repo to GitHub.
2. Create a new **Web Service** on [render.com](https://render.com) and point it at your repo.
3. Render will detect `backend/render.yaml` and configure the service automatically.
4. Add your secret environment variables in the Render dashboard (GEMINI_API_KEY, ELEVENLABS_API_KEY, MONGODB_URI).
5. Deploy — done! The backend URL becomes your frontend's `API` target.

For the frontend, deploy `frontend/` to **Vercel** (drag-and-drop or GitHub integration).

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health, model name, DB status |
| `POST` | `/api/generate-listing` | Gemma 4 full listing generation |
| `POST` | `/api/audio-pitch` | ElevenLabs MP3 voiceover synthesis |
| `POST` | `/api/listings/save` | Save listing to MongoDB Atlas |
| `GET` | `/api/listings?user_id=…` | Retrieve user-isolated saved listings |

Full interactive docs: `GET /docs` (Swagger UI).

---

## 💡 Why Open-Weight Gemma — The Business Case

| Concern | Closed Proprietary AI | Open-Weight Gemma in CraftOptima |
|---|---|---|
| **Merchant IP Privacy** | Product blueprints & craft techniques transmitted to corporate training servers | Zero data exfiltration — can run fully on-device or private VMs |
| **Unit Economics** | Per-token fees erode slim side-hustle margins (\$30–\$80/mo subscriptions) | Predictable hosting cost; free on local hardware (Ollama) |
| **API Vendor Lock-in** | Sudden deprecations or pricing hikes break your tool overnight | Open weights cannot be retroactively revoked or price-hiked |
| **Schema Compliance** | General-purpose APIs prone to prompt drift | Gemma 4 + `response_mime_type="application/json"` enforces strict output |

---

## 🏆 Hacktoberfest 2026 Sponsor Tracks

- **Best Use of Gemma** — `gemma-4-26b-a4b-it` via `google-genai` SDK for all structured inference
- **Best Use of Render** — Automated continuous deployment via `backend/render.yaml`
- **Best Use of MongoDB Atlas** — `motor` async driver with per-device tenant isolation
- **Best Use of ElevenLabs** — Neural TTS for 30-second audio commercials

Required challenge tag: `#hf26challenge`

---

## 📄 License

[MIT](./LICENSE) — open source, built for creator empowerment.
