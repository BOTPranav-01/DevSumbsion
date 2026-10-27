"""
NecroCode: The Open-Source Codebase Necromancer & Spectral Auditor.
Main FastAPI server entrypoint.
"""

import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.schemas import (
    RepoAnalysisRequest,
    SpectralAuditResult,
    ResurrectionPlan,
    SeanceRequest,
    SeanceResponse,
    GraveyardRecord
)
from app.core.necro_engine import necro_engine
from app.core.seance_agent import seance_agent
from app.core.voice_synthesizer import voice_synthesizer
from app.core.graveyard_vault import graveyard_vault
from app.core.telemetry import init_sentry, AgentSpanRecorder

# Initialize Sentry Agent Tracing
init_sentry()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>NecroCode: Ghost in the Machine</h1>")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "gemma_provider": settings.gemma_provider,
        "sentry_enabled": bool(settings.sentry_dsn),
        "elevenlabs_enabled": bool(settings.elevenlabs_api_key),
        "mongodb_enabled": bool(settings.mongodb_uri)
    }

@app.post("/api/audit")
async def audit_codebase(request: RepoAnalysisRequest):
    try:
        audit_result, spans = necro_engine.analyze_repository(request)
        return {
            "audit": audit_result,
            "telemetry_spans": spans
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resurrect")
async def resurrect_codebase(request: RepoAnalysisRequest):
    try:
        plan, spans = necro_engine.resurrect_repository(request)
        return {
            "plan": plan,
            "telemetry_spans": spans
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stream")
async def stream_pipeline(sample: str = "legacy_crypto"):
    request = RepoAnalysisRequest(preset_sample=sample, repo_name=sample)
    return StreamingResponse(
        necro_engine.stream_resurrection_pipeline(request),
        media_type="text/event-stream"
    )

@app.post("/api/seance", response_model=SeanceResponse)
async def summon_seance(req: SeanceRequest):
    recorder = AgentSpanRecorder()
    try:
        response = await seance_agent.invoke_seance(
            repo_name=req.repo_name,
            user_message=req.message,
            history=req.history,
            findings_context=req.findings_context,
            recorder=recorder
        )

        # Attempt ElevenLabs vocal synthesis
        audio_b64 = await voice_synthesizer.synthesize_spectral_voice(response.reply, recorder)
        response.audio_base64 = audio_b64
        response.agent_spans = recorder.spans

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/graveyard")
async def get_graveyard_records():
    return graveyard_vault.get_all_records()

@app.get("/api/samples")
async def get_samples_list():
    return [
        {
            "id": "legacy_crypto",
            "name": "Python 2 Cryptographic Tool (2012)",
            "description": "Afflicted with deprecated bare print statements, obsolete xrange, and broken MD5 collision hashing.",
            "rot_level": "CRITICAL"
        },
        {
            "id": "haunted_concurrency",
            "name": "Haunted Concurrency Worker Pool (2015)",
            "description": "Possessed by unsynchronized shared memory mutations, zombie threads, and CPU busy-spin loops.",
            "rot_level": "HAUNTED"
        },
        {
            "id": "abandoned_cli",
            "name": "Abandoned CLI Vault Tool (2016)",
            "description": "Riddled with insecure pickle deserialization, deprecated TLS 1.0 protocols, and shell execution.",
            "rot_level": "VULNERABLE"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
