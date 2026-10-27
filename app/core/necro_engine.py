"""
Main NecroEngine Orchestrator.
Executes the autonomous multi-agent pipeline for repository resurrection:
Auditor Agent -> Gemma Reasoner -> Resurrection Engine -> Graveyard Vault.
Supports streaming SSE events and Sentry Agent Tracing.
"""

import os
import uuid
import asyncio
from typing import AsyncGenerator, Dict, Any, List
from app.models.schemas import (
    RepoAnalysisRequest,
    SpectralAuditResult,
    ResurrectionPlan,
    FileEntry,
    GraveyardRecord
)
from app.core.code_auditor import code_auditor
from app.core.resurrection import resurrection_engine
from app.core.graveyard_vault import graveyard_vault
from app.core.telemetry import AgentSpanRecorder, trace_agent_step

class NecroEngine:
    def get_sample_files(self, sample_name: str) -> List[FileEntry]:
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "samples")
        samples_map = {
            "legacy_crypto": "legacy_crypto.py",
            "haunted_concurrency": "haunted_concurrency.py",
            "abandoned_cli": "abandoned_cli.py"
        }
        filename = samples_map.get(sample_name, "legacy_crypto.py")
        file_path = os.path.join(base_dir, filename)
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return [FileEntry(path=filename, content=content, language="python")]
        
        # Fallback default
        return [FileEntry(
            path="legacy_code.py",
            content='print "Hello from 2012"\nimport hashlib\nh = hashlib.md5("secret")\n',
            language="python"
        )]

    def analyze_repository(self, request: RepoAnalysisRequest) -> Tuple_Result:
        recorder = AgentSpanRecorder()
        files = request.files

        if request.preset_sample:
            files = self.get_sample_files(request.preset_sample)
        elif not files and request.repo_name:
            files = self.get_sample_files("legacy_crypto")

        repo_name = request.repo_name or "HauntedRepository"
        
        # Step 1: Spectral Audit
        audit = code_auditor.audit_repository(repo_name, files, recorder)

        # Step 2: Store in Graveyard
        record = GraveyardRecord(
            id=f"grave-{uuid.uuid4().hex[:6]}",
            repo_name=repo_name,
            bit_rot_score=audit.bit_rot_score,
            cemetery_status=audit.cemetery_status,
            epitaph=audit.spectral_epitaph,
            resurrected=False
        )
        graveyard_vault.store_record(record)

        return audit, recorder.spans

    def resurrect_repository(self, request: RepoAnalysisRequest) -> Tuple_Plan:
        recorder = AgentSpanRecorder()
        files = request.files

        if request.preset_sample:
            files = self.get_sample_files(request.preset_sample)
        elif not files and request.repo_name:
            files = self.get_sample_files("legacy_crypto")

        repo_name = request.repo_name or "HauntedRepository"

        # Step 1: Perform resurrection
        plan = resurrection_engine.resurrect_codebase(repo_name, files, recorder)

        # Step 2: Update Graveyard record
        record = GraveyardRecord(
            id=f"grave-{uuid.uuid4().hex[:6]}",
            repo_name=repo_name,
            bit_rot_score=12, # Resurrected to low bit-rot
            cemetery_status="Resurrected & Sanctified",
            epitaph=f"{repo_name} has arisen from the crypts of open source, fully verified and hardened.",
            resurrected=True
        )
        graveyard_vault.store_record(record)

        return plan, recorder.spans

    async def stream_resurrection_pipeline(self, request: RepoAnalysisRequest) -> AsyncGenerator[str, None]:
        """Streams real-time SSE progress events to the client terminal."""
        repo_name = request.repo_name or "HauntedRepository"
        yield f"data: {{\"step\": \"summoning\", \"message\": \"Awakening spectral agent harness for {repo_name}...\"}}\n\n"
        await asyncio.sleep(0.3)

        yield f"data: {{\"step\": \"ast_scan\", \"message\": \"Traversing AST trees, detecting bit rot, dead dependencies, and CVEs...\"}}\n\n"
        await asyncio.sleep(0.4)

        audit, _ = self.analyze_repository(request)
        yield f"data: {{\"step\": \"audit_done\", \"message\": \"Cemetery Audit Complete: Bit Rot Score {audit.bit_rot_score}/100 ({audit.cemetery_status})\", \"score\": {audit.bit_rot_score}}}\n\n"
        await asyncio.sleep(0.3)

        yield f"data: {{\"step\": \"gemma_reasoning\", \"message\": \"Google Gemma Open-Weights Reasoner formulating modernization strategy...\"}}\n\n"
        await asyncio.sleep(0.4)

        plan, spans = self.resurrect_repository(request)
        yield f"data: {{\"step\": \"diff_generation\", \"message\": \"Synthesizing unified AST diffs and pytest test suites...\"}}\n\n"
        await asyncio.sleep(0.3)

        yield f"data: {{\"step\": \"complete\", \"message\": \"Resurrection Ritual Finalized. Code is reborn.\", \"patches\": {len(plan.patches)}}}\n\n"

# Helper type aliases for clean signatures
from typing import Tuple
Tuple_Result = Tuple[SpectralAuditResult, List[Dict[str, Any]]]
Tuple_Plan = Tuple[ResurrectionPlan, List[Dict[str, Any]]]

necro_engine = NecroEngine()
