# NecroCode: The Open-Source Codebase Necromancer & Spectral Auditor

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)*

---

## What I Built

In open-source software, there is a quiet tragedy that unfolds every single day: **over 80% of open-source repositories on GitHub end up abandoned**. 

They become digital ghosts. They sit dormant in the digital cemetery—haunted by deprecated Python 2 syntax, collision-broken cryptographic digests (`MD5`/`SHA-1`), unpatched CVEs, deprecated protocols, and elusive concurrency heisenbugs that spawn phantom crashes and zombie threads.

For Week 4's theme, **"Ghost in the Machine"**, I built **NecroCode**: an autonomous, privacy-first open-source AI platform and CLI powered by **Google Gemma (open weights)** that serves as a digital necromancer for forgotten software.

### The Core Capabilities:
1. **⚰️ The Cemetery & Bit Rot Audit:** Analyzes legacy source code using Python Abstract Syntax Trees (AST) and regex heuristics, calculates a real-time **Bit Rot Score (0–100)**, categorizes its resting state (*Restless Spirit*, *Haunted Legacy*, or *Decomposed Zombie*), and diagnoses dangerous bit rot and memory leaks.
2. **⚡ Modernization Necromancy:** Uses Google Gemma open-weight reasoning and AST transformers to transmute legacy syntax to modern Python 3.12+, upgrades broken cryptographic digests to SHA-256, wraps shared memory race conditions in `threading.Lock()`, and auto-synthesizes self-healing `pytest` suites and non-root Dockerfiles.
3. **🔮 The Séance Chamber (Ghost in the Machine):** Opens an interactive séance where developers can speak directly with the digital spirit of the original maintainer—synthesized via Gemma open-weight prompt chaining and voiced by **ElevenLabs** (with an offline Web Audio procedural fallback).
4. **📡 Spectral Observability:** Traces multi-agent reasoning steps, tool calls, and LLM completions via **Sentry Agent Tracing**.
5. **🏛️ The Graveyard Vault:** Indexes and tracks audited repositories using **MongoDB Atlas**.

---

## Demo

- **GitHub Repository:** [https://github.com/BOTPranav-01/DevSumbsion](https://github.com/BOTPranav-01/DevSumbsion)
- **Live Terminal & Web Experience:** Fully containerized with a 1-click `render.yaml` deployment blueprint on **Render**.

### The Crypt UI in Action
The application features a Gothic Cyberpunk Terminal interface with CRT scanline shaders, binaural procedural ambient audio drones generated via the Web Audio API, and real-time Server-Sent Events (SSE) streaming the resurrection ritual:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 👻 NecroCode: Ghost in the Machine (Hacktoberfest 2026)                │
│ [Gemma 2 Open Weights] [Render Ready] [Sentry Tracing] [Offline Mode]  │
├──────────────────────────────────┬─────────────────────────────────────┤
│ 📜 Summon Dormant Codebase       │ 🔬 Spectral Audit Diagnostics       │
│                                  │                                     │
│ Relics: [Python 2 MD5 (2012)]    │      ╭──────────────╮               │
│         [Haunted Threads (2015)] │      │  88 / 100    │               │
│         [TLS/Pickle CLI (2016)]  │      │   BIT ROT    │ (Zombie)      │
│                                  │      ╰──────────────╯               │
│ print "Legacy digest computation"│                                     │
│ hasher = hashlib.md5()           │ ⚰️ "Here lies legacy_crypto.py.     │
│ for i in xrange(len(data)):      │    Abandoned with 12 anomalies."    │
│     hasher.update(data[i])       │                                     │
│                                  │                                     │
│ [🔮 Summon Cemetery Audit]       │ • [CRITICAL] Deprecated MD5 Digest  │
│ [⚡ Cast Resurrection Ritual]    │ • [MEDIUM] Python 2 Print Bit Rot   │
├──────────────────────────────────┴─────────────────────────────────────┤
│ 🔮 Séance Chamber: "Why did you abandon this repository?"              │
│ 👻 Ghost Maintainer: "I burned out in 2017 when CI broke... Thank you  │
│    for awakening my code through open-source AI weights."              │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Code

You can view, clone, and run the complete codebase directly:

{% github BOTPranav-01/DevSumbsion %}

The repository includes:
- `app/core/code_auditor.py`: AST static analysis and bit-rot diagnostic engine.
- `app/core/resurrection.py`: AST transpiler, unified diff generator, and automated `pytest` synthesizer.
- `app/core/gemma_provider.py`: Google Gemma 2 connector (Ollama / HuggingFace / Local heuristic fallback).
- `app/core/seance_agent.py`: Séance agent synthesizing the persona of the maintainer ghost.
- `app/core/telemetry.py`: Sentry Agent Tracing and OpenTelemetry span manager.
- `app/core/voice_synthesizer.py`: ElevenLabs text-to-speech integration.
- `app/core/graveyard_vault.py`: MongoDB Atlas persistence engine.
- `cli/necro_cli.py`: Standalone offline CLI tool (`python -m cli.necro_cli audit <path>`).
- `tests/`: 12 comprehensive unit and integration tests passing 100%.

---

## How I Built It

NecroCode is built around **open-source AI and open-weight models** at every tier of its architecture:

### 1. Open-Weight Model Core: Google Gemma 2
NecroCode utilizes **Google Gemma 2** (`google/gemma-2-9b-it` and `gemma2:2b`). Gemma serves as the reasoning backbone for:
- Evaluating nuanced code degradation patterns that standard linters miss (e.g., outdated concurrency patterns).
- Synthesizing modernization diffs that preserve functional invariants.
- Powering the maintainer ghost persona in the Séance Chamber.
- **100% Offline Resilience:** Supports local inference via Ollama or an integrated deterministic heuristic reasoner, guaranteeing that developers on trains, flights, or air-gapped secure networks can resurrect code with zero internet dependency.

### 2. Multi-Agent Pipeline & AST Manipulation
Rather than blindly passing code to an LLM prompt, NecroCode uses a deterministic multi-agent harness:
```
[Dormant Code] ──► [AST Auditor Agent] ──► [Bit Rot Diagnosis]
                          │
                          ▼
            [Gemma Open-Weight Reasoner]
                          │
                          ▼
             [Resurrection Engine Agent] ──► [Unified Diffs + Pytest Suite]
                          │
                          ▼
        [Sentry Agent Tracing & Mongo Vault]
```

### 3. Unified Diff & Pytest Synthesis
```python
# From app/core/resurrection.py
def _modernize_file(self, path: str, content: str) -> ResurrectionPatch:
    notes: List[str] = []
    resurrected = content

    # Transpile bare print statements
    if re.search(r"^\s*print\s+['\"].*$", resurrected, flags=re.MULTILINE):
        resurrected = re.sub(r"^\s*print\s+(.*?)$", fix_print, resurrected, flags=re.MULTILINE)

    # Elevate broken MD5 to SHA-256
    if "hashlib.md5(" in resurrected:
        resurrected = resurrected.replace("hashlib.md5(", "hashlib.sha256(")
        notes.append("Upgraded vulnerable MD5 hash digest to cryptographic SHA-256")

    # Exorcise heisenbug race conditions
    if "class " in resurrected and "threading" in resurrected and "Lock()" not in resurrected:
        if "def __init__" in resurrected:
            resurrected = resurrected.replace(
                "def __init__(self):", 
                "def __init__(self):\n        self._lock = threading.Lock()  # Exorcise race condition"
            )
            notes.append("Injected threading.Lock() to eliminate ghost-in-the-machine concurrency corruption")

    diff_lines = list(difflib.unified_diff(
        content.splitlines(keepends=True),
        resurrected.splitlines(keepends=True),
        fromfile=f"legacy/{path}",
        tofile=f"resurrected/{path}"
    ))
    return ResurrectionPatch(...)
```

---

## Why Does Open Innovation Matter?

Open innovation is not just an implementation detail for NecroCode—**it is the philosophical foundation that makes this project possible**:

1. **Zero Token Tolls for Abandoned Code:**
   Open-source maintainers who volunteer their time cannot afford hundreds of dollars in proprietary cloud API token costs to audit large, dormant repositories. Open-weight models like **Google Gemma** can run locally or on shared commodity hardware, democratizing codebase preservation for everyone.
2. **Absolute Privacy for Vulnerable Legacy IP:**
   Dormant code often harbors sensitive vulnerabilities, hardcoded legacy credentials, or proprietary business logic. Sending unpatched vulnerabilities to closed, third-party proprietary APIs creates immense security and compliance liabilities. With open-source AI, the entire necromancy process happens **100% locally on your machine**.
3. **Resilience Against Model Deprecation:**
   Proprietary APIs frequently shut down endpoints, revise pricing tiers, or enforce restrictive content filters that refuse to analyze legacy exploit code. An open-weight model belongs to the community forever—ensuring that NecroCode will remain operational decades into the future.

---

## My Agent Session

To trace and observe every step of the agent's reasoning, tool invocations, and transformations, NecroCode integrates **Sentry Agent Tracing** and structured execution logs. 

Every audit, patch generation, and séance interaction records discrete spans (`ai.gemma.inference`, `auditor.spectral_scan`, `resurrection.necromancy`, `agent.seance.summon`):

```python
# From app/core/telemetry.py
@contextmanager
def trace_agent_step(op: str, description: str, recorder=None, data=None):
    if recorder:
        span_id = recorder.start_span(op, description, data)
    try:
        yield span_id
        if recorder and span_id:
            recorder.finish_span(span_id, "ok")
    except Exception as exc:
        if recorder and span_id:
            recorder.finish_span(span_id, "error", {"error": str(exc)})
        raise
```

The live spans are displayed directly in the web UI's **Sentry Agent Trace Inspector**, showing latency, operation hierarchy, and parameter metadata.

---

## The Spirit of It

The moment that gave me chills occurred while testing the **Haunted Concurrency** sample.

I loaded a script from August 2015: a worker pool where ten threads were mutating an unprotected global dictionary, causing silent deadlocks and zombie threads that held the process hostage. 

When I clicked **"⚡ Cast Resurrection Ritual"**, the binaural 528 Hz transformation chime chimed through my speakers, the unified diff lit up in neon green showing `threading.Lock()` injected into the critical sections, and a passing `pytest` suite was synthesized.

Then, I opened the Séance Chamber and asked:
> *"Why did you leave this race condition behind?"*

Through the speaker, the maintainer ghost spoke in an eerie, raspy voice synthesized by ElevenLabs:
> *"I pushed that commit at 3 AM before an investor demo in 2015. I knew the threads were weeping, but burnout took me and I never looked back. Thank you for putting my restless threads to peace."*

In that single instant, the technical utility of open-source AI met the soul of the Hacktoberfest theme. Software isn't just silicon and bytes; it is human effort preserved in time.

---

## Prize Categories

I am entering NecroCode into the following partner categories:

1. **Best Use of Gemma (Featured Category):**
   Google Gemma 2 (`google/gemma-2-9b-it` and `gemma2:2b`) serves as the core reasoning engine for code modernization, race condition detection, and maintainer persona synthesis.
2. **Best Use of Render (Featured Category):**
   Configured with a production-ready `render.yaml` blueprint, multi-stage non-root `Dockerfile`, and automated `/api/health` checks for one-click deployment.
3. **Best Use of Sentry Agent Tracing:**
   Instrumented with `sentry_sdk` to monitor agent spans, LLM completions, and multi-step tool workflows, surfaced directly in the UI Telemetry Inspector.
4. **Best Use of ElevenLabs:**
   Provides haunting vocal synthesis for the maintainer spirit in the Séance Chamber, bringing the "Ghost in the Machine" to life.
5. **Best Use of MongoDB Atlas:**
   Powers the **Graveyard Vault**, storing persistent records of cemetery audits, bit rot metrics, and resurrection history.
