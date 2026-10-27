"""
Pydantic Schemas for NecroCode.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time

class FileEntry(BaseModel):
    path: str
    content: str
    language: Optional[str] = "python"

class RepoAnalysisRequest(BaseModel):
    repo_url: Optional[str] = None
    repo_name: Optional[str] = "UserLegacyCode"
    files: List[FileEntry] = Field(default_factory=list)
    preset_sample: Optional[str] = None # e.g. "legacy_python2_crypto", "haunted_race_condition", "abandoned_cli_tool"

class BitRotFinding(BaseModel):
    id: str
    category: str # "deprecated_syntax", "zombie_dependency", "heisenbug_race_condition", "security_vulnerability", "memory_leak"
    severity: str # "CRITICAL", "HIGH", "MEDIUM", "LOW", "SPECTRAL"
    file_path: str
    line_number: Optional[int] = None
    title: str
    description: str
    ghost_remedy: str
    cve_id: Optional[str] = None

class SpectralAuditResult(BaseModel):
    repo_name: str
    bit_rot_score: int = Field(ge=0, le=100, description="0 is pristine, 100 is decomposed zombie")
    cemetery_status: str # "Restless Spirit", "Decomposed Zombie", "Haunted Legacy", "Resurrected"
    years_dormant: float = 7.5
    total_files: int = 0
    total_lines: int = 0
    findings: List[BitRotFinding] = Field(default_factory=list)
    spectral_epitaph: str
    maintainer_ghost_persona: str
    open_innovation_verdict: str

class ResurrectionPatch(BaseModel):
    file_path: str
    original_code: str
    resurrected_code: str
    unified_diff: str
    modernization_notes: List[str] = Field(default_factory=list)
    generated_tests: Optional[str] = None

class ResurrectionPlan(BaseModel):
    repo_name: str
    success: bool = True
    patches: List[ResurrectionPatch] = Field(default_factory=list)
    resurrection_scroll: str # Markdown markdown of what was resurrected
    migration_steps: List[str] = Field(default_factory=list)
    dockerfile_modernized: Optional[str] = None
    ci_cd_workflow: Optional[str] = None

class SeanceChatMessage(BaseModel):
    role: str # "user", "ghost_maintainer", "system"
    content: str
    timestamp: float = Field(default_factory=time.time)
    spectral_mood: Optional[str] = "haunting" # "mournful", "vengeful", "enlightened", "relieved"

class SeanceRequest(BaseModel):
    repo_name: str
    message: str
    history: List[SeanceChatMessage] = Field(default_factory=list)
    findings_context: Optional[str] = None

class SeanceResponse(BaseModel):
    reply: str
    spectral_mood: str
    audio_base64: Optional[str] = None
    trace_id: Optional[str] = None
    agent_spans: List[Dict[str, Any]] = Field(default_factory=list)

class GraveyardRecord(BaseModel):
    id: str
    repo_name: str
    bit_rot_score: int
    cemetery_status: str
    created_at: float = Field(default_factory=time.time)
    epitaph: str
    resurrected: bool = False
