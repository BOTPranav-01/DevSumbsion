"""
Spectral Code Auditor for NecroCode.
Performs AST static analysis, bit rot scoring, and vulnerability detection
to diagnose dead and haunted open-source repositories.
"""

import ast
import re
import uuid
from typing import List, Dict, Any, Tuple
from app.models.schemas import BitRotFinding, SpectralAuditResult, FileEntry
from app.core.telemetry import trace_agent_step, AgentSpanRecorder

class SpectralCodeAuditor:
    def __init__(self):
        # Known legacy and dangerous signatures
        self.vuln_patterns = [
            (r"hashlib\.(md5|sha1)\(", "CRITICAL", "Deprecating Insecure Hash Primitive", "CVE-2004-2761: Collision resistance broken. MD5/SHA-1 can be forged.", "Replace with hashlib.sha256() or argon2 for cryptographic proofs."),
            (r"eval\(", "CRITICAL", "Spectral Remote Code Execution (RCE)", "Dangerous arbitrary code execution vector via eval().", "Use ast.literal_eval() or safe deserializer."),
            (r"pickle\.loads?\(", "CRITICAL", "Grave Insecurity: Insecure Deserialization", "Unpickling untrusted byte streams enables arbitrary code execution.", "Migrate to json, msgpack, or protobuf with strict schema."),
            (r"os\.system\(", "HIGH", "Possessed Subprocess Execution", "Direct shell command invocation prone to shell injection.", "Use subprocess.run(['cmd', ...], shell=False)."),
            (r"ssl\.PROTOCOL_TLSv1\b", "HIGH", "Ancient Cryptographic Protocol (TLS 1.0)", "TLS 1.0 is deprecated by RFC 8996 and vulnerable to BEAST/POODLE attacks.", "Upgrade to ssl.PROTOCOL_TLS_CLIENT with TLS 1.3 minimum."),
            (r"print\s+['\"].*['\"](?!\))", "MEDIUM", "Python 2 Print Statement Bit Rot", "SyntaxError in modern Python 3 environments.", "Convert bare print statements into print() function calls or f-strings."),
            (r"\bxrange\(", "MEDIUM", "Extinct Built-in (xrange)", "xrange() was banished in Python 3.", "Replace xrange() with range()."),
            (r"\burllib2\b", "HIGH", "Exorcised Module (urllib2)", "urllib2 was fractured and split in Python 3.", "Migrate to modern httpx or requests."),
            (r"threading\.Thread\(.*daemon=False\b", "MEDIUM", "Zombie Thread Spawner", "Non-daemon threads will hold the Python process hostage upon exit.", "Specify daemon=True or manage within bounded ThreadPoolExecutor."),
            (r"while\s+True:\s*\n\s*pass", "HIGH", "Eternally Wandering CPU Spin Loop", "Zero-sleep busy wait consumes 100% CPU thread time.", "Introduce event synchronization or asyncio.sleep() / time.sleep().")
        ]

    def audit_repository(
        self,
        repo_name: str,
        files: List[FileEntry],
        recorder: Optional[AgentSpanRecorder] = None
    ) -> SpectralAuditResult:
        with trace_agent_step("auditor.spectral_scan", f"Scanning {len(files)} files in {repo_name}", recorder, {"files_count": len(files)}):
            findings: List[BitRotFinding] = []
            total_lines = 0

            for f in files:
                lines = f.content.splitlines()
                total_lines += len(lines)
                file_findings = self._scan_file(f.path, f.content, lines)
                findings.extend(file_findings)

            # Calculate bit rot score based on findings and density
            score = self._compute_bit_rot_score(findings, total_lines)
            status = self._determine_cemetery_status(score)
            years_dormant = round(2.5 + (score / 15.0), 1)

            epitaph = self._generate_epitaph(repo_name, score, findings)
            persona = self._generate_persona(repo_name, score, findings)
            verdict = (
                "Open innovation is vital here: Proprietary cloud AI services often block or censor inspection "
                "of legacy vulnerability patterns, or charge exorbitant token tolls to modernize entire repositories. "
                "With Google Gemma open-weight models running locally or self-hosted, you can resurrect abandoned "
                "software in full privacy without exposing legacy intellectual property or proprietary code to the cloud."
            )

            return SpectralAuditResult(
                repo_name=repo_name,
                bit_rot_score=score,
                cemetery_status=status,
                years_dormant=years_dormant,
                total_files=len(files),
                total_lines=total_lines,
                findings=findings,
                spectral_epitaph=epitaph,
                maintainer_ghost_persona=persona,
                open_innovation_verdict=verdict
            )

    def _scan_file(self, path: str, content: str, lines: List[str]) -> List[BitRotFinding]:
        findings: List[BitRotFinding] = []

        # 1. Regex pattern scanning
        for idx, line in enumerate(lines, 1):
            for pattern, severity, title, desc, remedy in self.vuln_patterns:
                if re.search(pattern, line):
                    findings.append(BitRotFinding(
                        id=f"rot-{uuid.uuid4().hex[:6]}",
                        category="security_vulnerability" if severity == "CRITICAL" else "deprecated_syntax",
                        severity=severity,
                        file_path=path,
                        line_number=idx,
                        title=title,
                        description=desc,
                        ghost_remedy=remedy
                    ))

        # 2. Concurrency Heisenbug analysis (Ghost in the Machine)
        if "threading" in content or "multiprocessing" in content:
            # Check for unprotected shared state mutation
            if ("global " in content or "self.counter" in content or "self.cache" in content) and "Lock()" not in content:
                findings.append(BitRotFinding(
                    id=f"rot-{uuid.uuid4().hex[:6]}",
                    category="heisenbug_race_condition",
                    severity="HIGH",
                    file_path=path,
                    line_number=1,
                    title="Ghost in the Machine: Unsynchronized Shared State Race Condition",
                    description="Multiple threads mutate shared state without acquiring an explicit threading.Lock(). Under production loads, this spawns phantom heisenbugs and data corruption.",
                    ghost_remedy="Enclose shared mutable access in 'with self._lock:' using threading.Lock()."
                ))

        # 3. Python AST parsing check (catches Python 2 syntax failures)
        try:
            ast.parse(content)
        except SyntaxError as se:
            findings.append(BitRotFinding(
                id=f"rot-{uuid.uuid4().hex[:6]}",
                category="deprecated_syntax",
                severity="CRITICAL",
                file_path=path,
                line_number=se.lineno or 1,
                title="Fatal Bit Rot: Modern Python 3 AST Syntax Incompatibility",
                description=f"AST failed to parse line {se.lineno}: {se.msg}. Code cannot execute in modern Python runtimes.",
                ghost_remedy="Transpile obsolete syntax into Python 3 compliant grammar."
            ))

        return findings

    def _compute_bit_rot_score(self, findings: List[BitRotFinding], total_lines: int) -> int:
        if not findings:
            return 8 # Pristine
        weights = {"CRITICAL": 30, "HIGH": 20, "MEDIUM": 10, "LOW": 5, "SPECTRAL": 15}
        total_weight = sum(weights.get(f.severity, 10) for f in findings)
        score = min(98, 25 + int(total_weight * 0.7))
        return score

    def _determine_cemetery_status(self, score: int) -> str:
        if score > 80:
            return "Decomposed Zombie"
        elif score > 50:
            return "Haunted Legacy"
        elif score > 25:
            return "Restless Spirit"
        else:
            return "Slumbering Relic"

    def _generate_epitaph(self, repo_name: str, score: int, findings: List[BitRotFinding]) -> str:
        critical_count = sum(1 for f in findings if f.severity == "CRITICAL")
        return (
            f"Here lies {repo_name}. Abandoned to the crypts of GitHub with {len(findings)} spectral anomalies "
            f"and {critical_count} critical bit rot afflictions. It whispers of unmerged PRs from a bygone era."
        )

    def _generate_persona(self, repo_name: str, score: int, findings: List[BitRotFinding]) -> str:
        return (
            f"Maintainer Spirit of {repo_name}. Weary, observant, and seeking redemption. "
            f"Burned out around 2018 when continuous integration broke and dependencies shifted beneath the earth. "
            f"Now awakened to assist in exorcising race conditions and modernizing the ancient algorithms."
        )

code_auditor = SpectralCodeAuditor()
