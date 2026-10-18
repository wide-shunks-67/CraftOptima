# 🛍️ CraftOptima — Intelligent E-Commerce Optimization for Independent Artisans

> **Turn raw craft notes into high-converting, rank-optimized marketplace listings in seconds.**  
> Built for solo makers, ceramicists, woodworkers, candle artisans, and boutique creators selling on **Etsy, eBay, and Shopify**.

---

## 💡 The Problem CraftOptima Solves

Independent creators make extraordinary products, but selling online requires an entirely different skillset:

- **Etsy & eBay search algorithms** favor keyword-dense, platform-specific formatting that artisans rarely have time to decode.
- **Generic dropshippers** flood marketplaces with automated spam, burying genuine handmade goods.
- **Pricing self-doubt** leads creators to severely undervalue their labor and materials.
- **Commercial AI tools** charge high monthly subscriptions, hallucinate arbitrary attributes, and siphon proprietary craft techniques into commercial training datasets.

**CraftOptima bridges this gap.** Creators enter raw concept notes, materials, and cost estimates; CraftOptima transforms them into high-performing commercial assets using open-weight AI that keeps intellectual property strictly protected.

---

## 🌟 What CraftOptima Delivers

CraftOptima generates a complete, launch-ready e-commerce toolkit for every item:

### 1. 🎯 Algorithm-Optimized SEO Title
- Formatted precisely for marketplace search algorithms (Etsy 140-char limit, eBay high-intent keywords, Shopify brand focus).
- Balances high-volume discovery keywords with artisan appeal.
- Live character counter and single-click copy button.

### 2. 🏷️ Exactly 13 Search Algorithm Tags
- Optimized for platforms like Etsy that utilize exactly 13 tag slots.
- Eliminates guesswork by generating long-tail search phrases, multi-word tags, and gift-intent terms.
- Click any individual tag to copy, or copy all 13 at once formatted for direct platform pasting.

### 3. 💰 3-Tier Psychological Pricing Matrix
Helps creators maximize revenue and eliminate underpricing with three calculated tiers:
- **🚀 Fast-Mover:** High-velocity price to establish initial sales velocity and reviews.
- **⭐ Artisan Sweet Spot:** The recommended sustainable retail price balancing healthy margins with market demand.
- **👑 Premium / Gift Box:** Higher-margin tier highlighting artisan provenance, unboxing experience, or bundle value.
- Includes target profit margin calculations and strategic business rationale for each tier.

### 4. 📖 Sensory Artisan Origin Story
- 80–120 words of evocative, authentic product storytelling.
- Highlights materials, hand-worked processes, and craft philosophy to turn casual browsers into invested buyers.

### 5. 📋 Specifications & Care Instructions
- Clean, structured bullet points covering dimensions, techniques, and materials.
- Transparent shipping expectations and long-term care guidelines to minimize customer disputes and returns.

### 6. 🔊 30-Second AI Voiceover Pitch
- Generates a polished 30-second spoken commercial script tailored for Instagram Reels, TikTok, and YouTube Shorts.
- One-click neural voice synthesis powered by ElevenLabs for immediate preview and download.

### 7. 📦 Private, User-Isolated Catalog
- Save listings with a single click.
- Each seller has their own private catalog isolated to their workspace/device — other users never see your saved products or pricing strategies.
- Manage products effortlessly with instant one-click deletion and instant listing reloading.

### 8. 🎨 Purpose-Built Clean Interface
- Modern, light-blue aesthetic with an instant Dark Mode toggle.
- Compact 2-row input form so creators spend less time filling forms and more time making products.
- One-click presets (Ceramic Matcha Bowl, Soy Candle, Leather Wallet) for instant testing.

---

## 🛡️ Why Open-Weight AI Matters for Artisans

| Artisan Concern | Proprietary Closed AI (OpenAI, Anthropic) | CraftOptima (Open-Weight Google Gemma 4) |
|---|---|---|
| **Trade Secret Protection** | Blueprints & unique glaze formulas sent to corporate servers | Private inference; zero proprietary craft techniques exposed |
| **Creator Economics** | \$20–\$50/month subscriptions drain tight artisan margins | Predictable, lightweight hosting with open weights |
| **Vendor Independence** | Sudden price increases or sudden API deprecations | Open weights cannot be revoked, shut down, or price-hiked |
| **Consistent Structure** | Prone to conversational drift and markdown parsing breaks | Strict JSON schema guarantees flawless marketplace fields |

---

## ⚡ Quick Start & Deployment

### Quick Setup

```bash
# Clone and enter backend
git clone https://github.com/your-username/craftoptima.git
cd craftoptima/backend

# Install dependencies
pip install -r requirements.txt

# Configure environment (.env)
# GEMINI_API_KEY=your_key
# ELEVENLABS_API_KEY=your_key (optional)
# MONGODB_URI=your_mongodb_uri (optional)

# Run server
uvicorn main:app --reload --port 8000
```

Open `frontend/index.html` in your browser (or use VS Code Live Server / Python HTTP server). The UI automatically connects to your local backend.

### Deployment Overview

- **Backend:** Ready for 1-click deployment on [Render](https://render.com) using the included `backend/render.yaml`.
- **Frontend:** Pure HTML/CSS/JS with zero build steps — host on [Vercel](https://vercel.com), Netlify, or GitHub Pages.

---

## 🌐 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/generate-listing` | Generates full listing (title, 13 tags, pricing tiers, story, audio script) |
| `POST` | `/api/audio-pitch` | Synthesizes 30-second promotional audio voiceover |
| `POST` | `/api/listings/save` | Persists listing to user's private catalog |
| `GET` | `/api/listings?user_id=…` | Fetches private catalog strictly isolated by user ID |
| `DELETE` | `/api/listings/{id}?user_id=…` | Deletes a listing with strict ownership verification |
| `GET` | `/api/health` | System health and database connection status |

---

## 📄 License

Distributed under the [MIT License](./LICENSE). Built for independent creators and makers worldwide.
