"""
Configuration module for NecroCode.
Supports Google Gemma open-weight models, Sentry Agent Tracing,
ElevenLabs Spectral Voice, MongoDB Atlas Cemetery Vault, and Render deployment.
"""

import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    app_name: str = "NecroCode"
    app_version: str = "1.0.0"
    app_description: str = "The Open-Source Codebase Necromancer & Spectral Auditor (Ghost in the Machine)"
    
    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() in ("true", "1")
    
    # Google Gemma & Open AI Provider
    # Options: "ollama", "huggingface", "heuristic_local"
    gemma_provider: str = os.getenv("GEMMA_PROVIDER", "heuristic_local")
    gemma_model: str = os.getenv("GEMMA_MODEL", "google/gemma-2-9b-it")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    huggingface_token: str = os.getenv("HUGGINGFACE_TOKEN", "")
    
    # Sentry Agent Tracing
    sentry_dsn: str = os.getenv("SENTRY_DSN", "")
    sentry_traces_sample_rate: float = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0"))
    
    # ElevenLabs Spectral Audio
    elevenlabs_api_key: str = os.getenv("ELEVENLABS_API_KEY", "")
    elevenlabs_voice_id: str = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB") # Adam / Deep Raspy Ghost
    
    # MongoDB Atlas Graveyard Vault
    mongodb_uri: str = os.getenv("MONGODB_URI", "")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "necrocode_graveyard")
    
    # Render Platform detection
    is_render: bool = "RENDER" in os.environ

settings = Settings()
