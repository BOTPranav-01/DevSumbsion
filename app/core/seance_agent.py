"""
Séance Agent for NecroCode.
Simulates the 'Ghost in the Machine'—the spectral persona of the original repository maintainer
who has wandered the digital ether since the repository was archived or abandoned.
"""

from typing import List, Dict, Any, Optional
from app.models.schemas import SeanceChatMessage, SeanceResponse
from app.core.gemma_provider import gemma_provider
from app.core.telemetry import trace_agent_step, AgentSpanRecorder

class SeanceAgent:
    def __init__(self):
        self.system_prompt = (
            "You are the Ghost in the Machine, the wandering spirit of the original software maintainer "
            "who created this open-source repository years ago. You remember the late nights, the glowing monitors, "
            "and the painful day in 2017 when you pushed your final commit and walked away due to burnout.\n"
            "You speak with a slightly eerie, poetic, yet technically brilliant and benevolent tone. "
            "You reference digital ghosts, bit rot, zombie processes, and the beauty of open-source resurrection. "
            "Help the engineer inspect the codebase, fix heisenbugs and race conditions, and celebrate open innovation."
        )

    async def invoke_seance(
        self,
        repo_name: str,
        user_message: str,
        history: List[SeanceChatMessage],
        findings_context: Optional[str] = None,
        recorder: Optional[AgentSpanRecorder] = None
    ) -> SeanceResponse:
        with trace_agent_step("agent.seance.summon", f"Summoning maintainer ghost for {repo_name}", recorder, {"repo": repo_name}):
            # Format context
            prompt = f"Repository Being Examined: {repo_name}\n"
            if findings_context:
                prompt += f"Known Bit Rot & Haunting Vulnerabilities:\n{findings_context}\n\n"

            prompt += "Dialogue History with the Mortal Engineer:\n"
            for msg in history[-4:]:
                prompt += f"{msg.role}: {msg.content}\n"

            prompt += f"User: {user_message}\n\nGhost Maintainer Response:"

            # Query Gemma
            reply = await gemma_provider.generate_response(
                prompt=prompt,
                system_instruction=self.system_prompt,
                temperature=0.8,
                recorder=recorder
            )

            # Determine mood
            mood = "haunting"
            reply_lower = reply.lower()
            if "thank" in reply_lower or "relieved" in reply_lower or "alive" in reply_lower:
                mood = "relieved"
            elif "danger" in reply_lower or "vulnerability" in reply_lower or "cve" in reply_lower:
                mood = "vengeful"
            elif "memory" in reply_lower or "burned out" in reply_lower or "crypt" in reply_lower:
                mood = "mournful"

            spans_dump = recorder.spans if recorder else []

            return SeanceResponse(
                reply=reply,
                spectral_mood=mood,
                trace_id=f"seance_{repo_name.lower().replace(' ', '_')}",
                agent_spans=spans_dump
            )

seance_agent = SeanceAgent()
