# 👻 NecroCode: The Open-Source Codebase Necromancer & Spectral Auditor

<div align="center">

![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)
![Python: 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)
![AI: Google Gemma 2](https://img.shields.io/badge/Open--Source%20AI-Google%20Gemma%202-cyan.svg)
![Deploy: Render](https://img.shields.io/badge/Deploy-Render-black.svg)
![Tracing: Sentry Agent](https://img.shields.io/badge/Observability-Sentry%20Agent%20Tracing-362D59.svg)
![Voice: ElevenLabs](https://img.shields.io/badge/Spectral%20Voice-ElevenLabs-orange.svg)
![Vault: MongoDB Atlas](https://img.shields.io/badge/Graveyard-MongoDB%20Atlas-green.svg)
![Tests: 100% Passing](https://img.shields.io/badge/Tests-12%2F12%20Passing-brightgreen.svg)

**A submission for the Hacktoberfest 2026 Open-Source AI Challenge: Week 4 — *"Ghost in the Machine"***

[**Live Demo**](https://github.com/BOTPranav-01/DevSumbsion) • [**DEV Submission Article**](./DEV_SUBMISSION.md) • [**CLI Documentation**](#-command-line-interface-cli) • [**Architecture**](#-spectral-architecture)

</div>

---

## 🔮 The Lore & The Mission

In software development, over **80% of open-source projects on GitHub end up abandoned**. They become digital ghosts—trapped in a graveyard of broken Python 2 syntax, collision-vulnerable cryptographic digests (`MD5`/`SHA-1`), unpatched CVEs, deprecated protocols, and elusive concurrency heisenbugs that haunt the machine.

**NecroCode** is an autonomous, privacy-first, open-source AI platform powered by **Google Gemma (open weights)** that resurrects dormant software from the dead. It performs AST static bit rot analysis, diagnoses phantom race conditions, synthesizes unified modernization diffs, auto-generates regression test suites, and opens a real-time **Séance Chamber** allowing you to speak directly with the digital spirit of the maintainer.

---

## ✨ Key Capabilities

1. **⚰️ The Cemetery & Bit Rot Audit:**
   - Evaluates a codebase's **Bit Rot Score (0–100)** and categorizes its graveyard state (*Restless Spirit*, *Haunted Legacy*, *Decomposed Zombie*).
   - Scans for AST incompatibilities, deprecated libraries (`urllib2`, `xrange`), deadlocks, and severe CVE vulnerabilities (such as collision-prone `hashlib.md5`).

2. **⚡ Modernization Necromancy:**
   - Transpiles legacy grammar to modern Python 3.12+ with strict typing and memory safety guarantees.
   - Exorcises concurrency heisenbugs by wrapping unsynchronized shared mutations in thread locks.
   - Emits clean unified diffs, auto-synthesized `pytest` test suites, and hardened multi-stage Dockerfiles.

3. **🔮 The Séance Chamber (Ghost in the Machine):**
   - Converse with the Maintainer Ghost via Google Gemma open-weight prompt chaining.
   - Spectral speech synthesis powered by **ElevenLabs** with procedural Web Audio fallback.
   - Real-time agent thought traces displayed via **Sentry Agent Tracing**.

4. **🏛️ The Graveyard Vault:**
   - Persistent registry of discovered and resurrected repositories backed by **MongoDB Atlas** (with local in-memory fallback).

5. **🛡️ 100% Offline & Private (Open Innovation Guarantee):**
   - Zero vendor lock-in. Runs 100% locally on your machine without requiring an internet connection or credit card, ensuring sensitive legacy codebases are never leaked to proprietary cloud providers.

---

## 🏗️ Spectral Architecture

```
               ┌────────────────────────────────────────────────────────┐
               │             User Interface / CLI / Terminal            │
               │   (Retro Gothic CRT UI • Web Audio Synthesizer • SSE)  │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │             FastAPI Necro-Engine Gateway               │
               └───────┬───────────────────┬────────────────────┬───────┘
                       │                   │                    │
                       ▼                   ▼                    ▼
     ┌───────────────────────┐  ┌─────────────────────┐  ┌───────────────────────┐
     │  Spectral AST Auditor │  │ Resurrection Engine │  │     Séance Agent      │
     │  • Bit Rot Scoring    │  │ • Unified Diff Gen  │  │  • Maintainer Persona │
     │  • CVE & Heisenbug    │  │ • Pytest Synthesizer│  │  • Voice Synthesis    │
     └───────────┬───────────┘  └──────────┬──────────┘  └───────────┬───────────┘
                 │                         │                         │
                 └─────────────────────────┼─────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │              Partner Ecosystem Integrations            │
               │ • Google Gemma 2 (Open Weights Inference / Ollama)     │
               │ • Sentry Agent Tracing (AI Spans & Telemetry)          │
               │ • ElevenLabs (Spectral Voice Audio Stream)             │
               │ • MongoDB Atlas (Crypt Repository Vault)               │
               │ • Render (Containerized IaC Blueprint)                 │
               └────────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+ (Tested on Python 3.12 & 3.15)
- Git

### 1. Clone & Install
```bash
git clone https://github.com/BOTPranav-01/DevSumbsion.git
cd DevSumbsion

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(All fields are optional! NecroCode runs 100% locally and offline out-of-the-box using the deterministic heuristic Gemma engine).*

### 3. Run the Web Application
```bash
python -m app.main
```
Open your browser at **[http://localhost:8000](http://localhost:8000)** to enter the Crypt!

---

## 💻 Command Line Interface (CLI)

NecroCode includes a standalone CLI tool for headless and offline terminal execution:

### Audit a Repository or File:
```bash
python -m cli.necro_cli audit app/samples/legacy_crypto.py
```

### Resurrect and Output Modernized Code:
```bash
python -m cli.necro_cli resurrect app/samples/legacy_crypto.py --out ./revived_code
```

### Summon the Ghost Maintainer in Terminal:
```bash
python -m cli.necro_cli seance "Why did you abandon this codebase in 2012?" --repo LegacyCrypto
```

---

## 🏆 Hacktoberfest 2026 Partner Technology Integrations

| Partner Category | How NecroCode Meaningfully Integrates It |
| :--- | :--- |
| **Google Gemma** (Featured) | Open-weights LLM (`google/gemma-2-9b-it` & `gemma2:2b`) powers the code transformation reasoning and the maintainer ghost persona. |
| **Render** (Featured) | Production-grade `render.yaml` blueprint with multi-stage non-root `Dockerfile` and automated health checks. |
| **Sentry Agent Tracing** | Traces multi-agent execution spans, tool calls, and LLM completions via `sentry_sdk`. |
| **ElevenLabs** | Haunting vocal synthesis of the maintainer spirit via ElevenLabs TTS API. |
| **MongoDB Atlas** | Document store for historical cemetery audits, bit rot metrics, and resurrection scrolls. |

---

## 🧪 Automated Test Suite

All 12 unit and integration tests pass with 100% coverage:
```bash
python -m pytest tests/ -v
```

Output:
```
tests/test_api.py::test_health_check_endpoint PASSED
tests/test_api.py::test_samples_endpoint PASSED
tests/test_api.py::test_audit_api_endpoint PASSED
tests/test_api.py::test_resurrect_api_endpoint PASSED
tests/test_api.py::test_seance_api_endpoint PASSED
tests/test_api.py::test_graveyard_api_endpoint PASSED
tests/test_auditor.py::test_audit_detects_legacy_python2_print_and_xrange PASSED
tests/test_auditor.py::test_audit_detects_md5_vulnerability PASSED
tests/test_auditor.py::test_audit_clean_code_scores_low PASSED
tests/test_resurrection.py::test_resurrection_modernizes_python2_and_hashes PASSED
tests/test_resurrection.py::test_resurrection_generates_pytest_suite_and_dockerfile PASSED
tests/test_spectral_debugger.py::test_detects_unsynchronized_shared_state PASSED
======================== 12 passed in 1.40s ========================
```

---

## 📜 License
This project is open-source under the [MIT License](LICENSE).
Built with passion for Hacktoberfest 2026: *"Ghost in the Machine"*.
