"""
CraftOptima – Backend API (main.py)
====================================
FastAPI ASGI server powering the CraftOptima open-weight AI listing optimizer.

Endpoints:
  GET  /api/health              – health check
  POST /api/generate-listing    – Gemma 4 listing generation (title, tags, pricing, story, audio script)
  POST /api/audio-pitch         – ElevenLabs TTS voiceover synthesis (returns audio/mpeg)
  POST /api/listings/save       – save an optimized listing to MongoDB Atlas
  GET  /api/listings            – retrieve saved listings for a device-isolated user

Open-source AI core: google-genai SDK with open-weight model gemma-4-26b-a4b-it
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel, Field

from google import genai
from google.genai import types

# ──────────────────────────────────────────────────────────
# Startup
# ──────────────────────────────────────────────────────────

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)
logger = logging.getLogger("craftoptima")

app = FastAPI(
    title="CraftOptima API",
    description=(
        "Open-Weight AI Listing & SEO Optimizer for independent artisans on "
        "Etsy, eBay, and Shopify. Powered by Google Gemma 4."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────
# Google GenAI client (Gemma 4 open-weight model)
# ──────────────────────────────────────────────────────────

GEMMA_MODEL = "gemma-4-26b-a4b-it"

try:
    gemini_client = genai.Client()
    logger.info("Google GenAI client initialised (model: %s)", GEMMA_MODEL)
except Exception as exc:
    logger.warning("Could not initialise GenAI client: %s", exc)
    gemini_client = None

# ──────────────────────────────────────────────────────────
# MongoDB Atlas (motor async driver) with in-memory fallback
# ──────────────────────────────────────────────────────────

MONGODB_URI = os.getenv("MONGODB_URI", "")
catalog_collection = None
_in_memory_catalog: List[Dict[str, Any]] = []

if MONGODB_URI:
    try:
        from motor.motor_asyncio import AsyncIOMotorClient

        _mongo_client = AsyncIOMotorClient(MONGODB_URI)
        _db = _mongo_client[os.getenv("MONGODB_DB_NAME", "craftoptima_db")]
        catalog_collection = _db["listings"]
        logger.info("Connected to MongoDB Atlas.")
    except Exception as exc:
        logger.warning("MongoDB Atlas connection failed, using in-memory store: %s", exc)

# ──────────────────────────────────────────────────────────
# System instruction for Gemma
# ──────────────────────────────────────────────────────────

SYSTEM_INSTRUCTION = """
You are CraftOptima, an elite e-commerce listing strategist and copywriter built
with Google's open-weight Gemma model. You exist to empower independent artisans,
makers, and solo side-hustlers to out-rank and out-sell mass-market dropshippers
on Etsy, eBay, and Shopify.

Given a seller's raw product notes you MUST produce a JSON object with these
exact keys (no extra keys, no markdown fences):

{
  "optimized_title": string,           // SEO-dense, platform-aware title
  "seo_tags": [string × 13],           // EXACTLY 13 tags, no # prefix
  "suggested_categories": [string],    // 2–3 platform categories
  "pricing_strategy": {
    "currency": "USD",
    "recommended_retail": number,
    "profit_margin_target": string,    // e.g. "65%"
    "pricing_tiers": [
      {"tier_name": string, "price": number, "rationale": string},
      {"tier_name": string, "price": number, "rationale": string},
      {"tier_name": string, "price": number, "rationale": string}
    ]
  },
  "compelling_story": string,          // 80–120 word emotive origin story
  "bullet_features": [string],         // 5–7 concise spec bullets
  "shipping_and_care_tips": string,    // 2–3 sentences
  "platform_spec": {
    "platform": string,
    "title_char_count": number,
    "tag_strategy": string             // brief explanation of tagging approach
  },
  "audio_pitch_script": string,        // ≤30-second spoken commercial script
  "open_innovation_rationale": string  // why open-weight Gemma protects artisan margin & IP
}

Rules:
- seo_tags must contain EXACTLY 13 items. Count carefully.
- pricing_tiers must contain EXACTLY 3 items.
- Respond with valid JSON ONLY. No preamble, no markdown.
""".strip()

# ──────────────────────────────────────────────────────────
# Pydantic models
# ──────────────────────────────────────────────────────────


class ListingRequest(BaseModel):
    product_name: str = Field(..., description="Raw product name / concept")
    materials: Optional[str] = Field(None, description="Materials or craft method")
    target_platform: str = Field("Etsy", description="Etsy | eBay | Shopify")
    target_audience: Optional[str] = Field(
        "Eco-conscious buyers and gift shoppers",
        description="Buyer persona description",
    )
    key_features: Optional[str] = Field(None, description="Unique features / dimensions")
    current_price_estimate: Optional[float] = Field(
        None, description="Seller's cost or rough price estimate (USD)"
    )
    user_id: str = Field("anon-seller", description="Anonymous device identifier")


class PricingTier(BaseModel):
    tier_name: str
    price: float
    rationale: str


class PricingStrategy(BaseModel):
    currency: str
    recommended_retail: float
    profit_margin_target: str
    pricing_tiers: List[PricingTier]


class PlatformSpec(BaseModel):
    platform: str
    title_char_count: int
    tag_strategy: str


class ListingResponse(BaseModel):
    optimized_title: str
    seo_tags: List[str]
    suggested_categories: List[str]
    pricing_strategy: PricingStrategy
    compelling_story: str
    bullet_features: List[str]
    shipping_and_care_tips: str
    platform_spec: PlatformSpec
    audio_pitch_script: str
    open_innovation_rationale: str


class AudioPitchRequest(BaseModel):
    text: str = Field(..., description="Script text to synthesise")
    voice_id: str = Field(
        default_factory=lambda: os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
    )


class SaveListingRequest(BaseModel):
    user_id: str
    product_name: str
    platform: str
    data: Dict[str, Any]


# ──────────────────────────────────────────────────────────
# Helper: sanitise Gemma output → clean JSON string
# ──────────────────────────────────────────────────────────


def _clean_json(raw: str) -> str:
    """Strip any accidental markdown code fences from the model response."""
    text = raw.strip()
    for fence in ("```json", "```"):
        if text.startswith(fence):
            text = text[len(fence):]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


# ──────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────


@app.get("/api/health", tags=["System"])
async def health_check() -> Dict[str, Any]:
    """Returns service health status."""
    return {
        "status": "healthy",
        "service": "CraftOptima API",
        "model": GEMMA_MODEL,
        "mongodb_connected": catalog_collection is not None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/generate-listing", response_model=ListingResponse, tags=["Listings"])
async def generate_listing(req: ListingRequest) -> ListingResponse:
    """
    Calls Gemma 4 to generate a complete, platform-optimised product listing.
    Returns: SEO title, 13 search tags, 3-tier pricing, artisan story, audio script.
    """
    if not gemini_client:
        raise HTTPException(
            status_code=503,
            detail="Gemini client unavailable. Ensure GEMINI_API_KEY is configured.",
        )

    price_note = (
        f"${req.current_price_estimate:.2f}" if req.current_price_estimate else "market rate"
    )

    user_prompt = f"""
Platform: {req.target_platform}
Product: {req.product_name}
Materials / Craft Method: {req.materials or 'Handcrafted, artisan-made'}
Target Buyer Persona: {req.target_audience}
Key Features / Dimensions: {req.key_features or 'Unique handmade creation'}
Seller's Cost Estimate: {price_note}

Generate the complete JSON response now.
""".strip()

    try:
        response = gemini_client.models.generate_content(
            model=GEMMA_MODEL,
            contents=[SYSTEM_INSTRUCTION, user_prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7,
                max_output_tokens=4096,
            ),
        )
        cleaned = _clean_json(response.text)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback for unescaped newlines/control characters inside JSON strings
            parsed = json.loads(cleaned, strict=False)

        # Enforce tag count – trim or pad so Pydantic doesn't reject
        tags = parsed.get("seo_tags", [])
        if len(tags) > 13:
            parsed["seo_tags"] = tags[:13]
        elif len(tags) < 13:
            parsed["seo_tags"] = tags + [req.product_name.lower()] * (13 - len(tags))

        # Enforce exactly 3 pricing tiers
        tiers = parsed.get("pricing_strategy", {}).get("pricing_tiers", [])
        if len(tiers) > 3:
            parsed["pricing_strategy"]["pricing_tiers"] = tiers[:3]

        return ListingResponse(**parsed)

    except json.JSONDecodeError as exc:
        logger.error("Gemma returned invalid JSON: %s", exc)
        raise HTTPException(status_code=502, detail=f"Model returned malformed JSON: {exc}")
    except Exception as exc:
        logger.error("Listing generation error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/audio-pitch", tags=["Audio"])
async def audio_pitch(req: AudioPitchRequest) -> Response:
    """
    Synthesises a 30-second MP3 voiceover using ElevenLabs TTS.
    Returns audio/mpeg bytes directly for browser <audio> playback.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="ELEVENLABS_API_KEY is not configured on the server.",
        )

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{req.voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": req.text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, headers=headers, json=payload)

    if resp.status_code != 200:
        logger.error("ElevenLabs error %s: %s", resp.status_code, resp.text[:300])
        raise HTTPException(
            status_code=resp.status_code,
            detail="ElevenLabs voice synthesis failed.",
        )

    return Response(content=resp.content, media_type="audio/mpeg")


@app.post("/api/listings/save", tags=["Catalog"])
async def save_listing(req: SaveListingRequest) -> Dict[str, Any]:
    """Persists an optimised listing to MongoDB Atlas (or in-memory fallback)."""
    document = {
        "user_id": req.user_id,
        "product_name": req.product_name,
        "platform": req.platform,
        "data": req.data,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    if catalog_collection is not None:
        try:
            result = await catalog_collection.insert_one(document)
            return {
                "status": "success",
                "id": str(result.inserted_id),
                "storage": "mongodb_atlas",
            }
        except Exception as exc:
            logger.warning("MongoDB write failed, falling back to memory: %s", exc)

    _in_memory_catalog.append(document)
    return {
        "status": "success",
        "id": str(len(_in_memory_catalog) - 1),
        "storage": "in_memory",
    }


@app.get("/api/listings", tags=["Catalog"])
async def list_listings(user_id: str = Query("anon-seller")) -> Dict[str, Any]:
    """Returns saved listings isolated strictly by the caller's user_id."""
    if catalog_collection is not None:
        try:
            cursor = catalog_collection.find({"user_id": user_id}).sort("created_at", -1)
            items = []
            async for doc in cursor:
                doc["id"] = str(doc.pop("_id"))
                items.append(doc)
            return {"listings": items, "storage": "mongodb_atlas"}
        except Exception as exc:
            logger.warning("MongoDB query failed, using memory: %s", exc)

    items = [d for d in _in_memory_catalog if d.get("user_id") == user_id]
    return {"listings": list(reversed(items)), "storage": "in_memory"}


@app.delete("/api/listings/{listing_id}", tags=["Catalog"])
async def delete_listing(listing_id: str, user_id: str = Query(...)) -> Dict[str, Any]:
    """
    Deletes a single listing by ID — ONLY if it belongs to the requesting user_id.
    The user_id ownership check ensures no user can delete another user's data.
    """
    if catalog_collection is not None:
        try:
            from bson import ObjectId
            from bson.errors import InvalidId

            try:
                oid = ObjectId(listing_id)
            except InvalidId:
                raise HTTPException(status_code=400, detail="Invalid listing ID format.")

            result = await catalog_collection.delete_one(
                {"_id": oid, "user_id": user_id}  # ownership guard
            )
            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Listing not found or you do not have permission to delete it.",
                )
            return {"status": "deleted", "id": listing_id, "storage": "mongodb_atlas"}
        except HTTPException:
            raise
        except Exception as exc:
            logger.warning("MongoDB delete failed, trying memory fallback: %s", exc)

    # In-memory fallback — match by position index and user_id
    global _in_memory_catalog
    original_len = len(_in_memory_catalog)
    try:
        idx = int(listing_id)
        if 0 <= idx < original_len and _in_memory_catalog[idx].get("user_id") == user_id:
            _in_memory_catalog.pop(idx)
        else:
            raise HTTPException(status_code=404, detail="Listing not found.")
    except (ValueError, IndexError):
        raise HTTPException(status_code=404, detail="Listing not found.")
    return {"status": "deleted", "id": listing_id, "storage": "in_memory"}
