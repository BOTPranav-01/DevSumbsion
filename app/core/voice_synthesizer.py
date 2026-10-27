"""
Spectral Voice Synthesizer for NecroCode.
Supports ElevenLabs Text-to-Speech API for generating haunting vocalizations
of the codebase maintainer spirit, with automatic Web Audio procedural fallback.
"""

import base64
import logging
import httpx
from typing import Optional
from app.config import settings
from app.core.telemetry import trace_agent_step, AgentSpanRecorder

logger = logging.getLogger("necrocode.voice")

class VoiceSynthesizer:
    def __init__(self):
        self.api_key = settings.elevenlabs_api_key
        self.voice_id = settings.elevenlabs_voice_id

    async def synthesize_spectral_voice(
        self,
        text: str,
        recorder: Optional[AgentSpanRecorder] = None
    ) -> Optional[str]:
        """Synthesizes voice via ElevenLabs API, returning base64 encoded audio/mpeg string."""
        if not self.api_key:
            return None # Frontend will execute procedural Web Audio spectral TTS

        with trace_agent_step("audio.elevenlabs.tts", "Synthesizing ghost voice via ElevenLabs", recorder, {"voice_id": self.voice_id}):
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            payload = {
                "text": text[:500], # Keep concise for performance
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.35, # Spooky variability
                    "similarity_boost": 0.75,
                    "style": 0.55
                }
            }

            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 200:
                        b64_audio = base64.b64encode(resp.content).decode("utf-8")
                        return b64_audio
                    else:
                        logger.warning(f"ElevenLabs TTS returned status {resp.status_code}: {resp.text}")
            except Exception as e:
                logger.error(f"ElevenLabs voice synthesis error: {e}")

        return None

voice_synthesizer = VoiceSynthesizer()
