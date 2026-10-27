/**
 * NecroCode Main Frontend Application Controller.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Navigation Tabs
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));

      btn.classList.add("active");
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add("active");

      if (btn.dataset.tab === "vault-tab") {
        loadGraveyardRecords();
      }
    });
  });

  // State
  let currentSample = "legacy_crypto";
  let latestAudit = null;
  let latestPlan = null;
  let chatHistory = [];

  // Elements
  const sampleChips = document.querySelectorAll(".preset-chip");
  const codeArea = document.getElementById("code-area");
  const btnAudit = document.getElementById("btn-audit");
  const btnResurrect = document.getElementById("btn-resurrect");
  const btnAmbient = document.getElementById("btn-ambient");

  // Sample Presets Code
  const sampleCodes = {
    legacy_crypto: `#!/usr/bin/env python
# Legacy Cryptographic Service (Last updated: Oct 2012)
import hashlib
import urllib2

def generate_legacy_digest(payload):
    print "Generating legacy checksum for payload..."
    # VULNERABILITY: Insecure MD5 hash function
    hasher = hashlib.md5()
    for i in xrange(len(payload)):
        hasher.update(payload[i])
    digest = hasher.hexdigest()
    print "Computed digest: %s" % digest
    return digest

def fetch_remote_revocation_list(url):
    print "Connecting via deprecated urllib2..."
    req = urllib2.Request(url)
    return urllib2.urlopen(req).read()
`,
    haunted_concurrency: `#!/usr/bin/env python
# Haunted Concurrency Worker Pool (Last updated: Aug 2015)
import threading
import time

class HauntedWorkerPool:
    def __init__(self):
        # GHOST IN THE MACHINE: No Lock protecting shared counter!
        self.shared_counter = 0

    def spooky_mutation(self, thread_id):
        # Phantom read and race condition heisenbug
        current = self.shared_counter
        time.sleep(0.001)
        self.shared_counter = current + 1

    def spawn_zombie_threads(self, count=10):
        # VULNERABILITY: Non-daemon thread leak
        for i in range(count):
            t = threading.Thread(target=self.spooky_mutation, args=(i,), daemon=False)
            t.start()
`,
    abandoned_cli: `#!/usr/bin/env python
# Abandoned CLI Vault Tool (Last updated: Nov 2016)
import ssl
import os
import pickle

def authenticate_session(token):
    # VULNERABILITY: Outdated TLS 1.0 protocol
    return ssl.SSLContext(ssl.PROTOCOL_TLSv1)

def restore_cached_session(cache_file):
    # VULNERABILITY: Arbitrary code execution via pickle
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.loads(f.read())
    return None
`
  };

  // Set default code
  codeArea.value = sampleCodes.legacy_crypto;

  sampleChips.forEach(chip => {
    chip.addEventListener("click", () => {
      sampleChips.forEach(c => c.classList.remove("selected"));
      chip.classList.add("selected");
      currentSample = chip.dataset.sample;
      codeArea.value = sampleCodes[currentSample] || "";
    });
  });

  // Audio Ambient Toggle
  btnAmbient?.addEventListener("click", () => {
    const isPlaying = window.spectralAudio.toggleAmbientDrone();
    btnAmbient.classList.toggle("badge-active", isPlaying);
    btnAmbient.textContent = isPlaying ? "🔊 Crypt Atmosphere: Active" : "🔇 Crypt Atmosphere: Muted";
  });

  // Perform Audit
  btnAudit?.addEventListener("click", async () => {
    btnAudit.disabled = true;
    btnAudit.textContent = "Summoning Spirits...";

    try {
      const resp = await fetch("/api/audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repo_name: currentSample,
          files: [{ path: `${currentSample}.py`, content: codeArea.value, language: "python" }]
        })
      });

      const data = await resp.json();
      latestAudit = data.audit;
      renderAuditResults(data.audit);
      renderTelemetrySpans(data.telemetry_spans);

      // Pre-fill findings context for séance
      const findingsSummary = latestAudit.findings.map(f => `[${f.severity}] ${f.title}`).join(", ");
      document.getElementById("findings-context-tag").textContent = `Context: ${latestAudit.findings.length} spectral anomalies detected`;
    } catch (err) {
      console.error("Audit error:", err);
      alert("Error conducting spectral audit. Check server console.");
    } finally {
      btnAudit.disabled = false;
      btnAudit.textContent = "🔮 Summon Cemetery Audit";
    }
  });

  function renderAuditResults(audit) {
    const rotNum = document.getElementById("rot-score-num");
    const rotCircle = document.getElementById("rot-score-circle");
    const statusText = document.getElementById("cemetery-status-text");
    const yearsText = document.getElementById("years-dormant-text");
    const epitaphText = document.getElementById("spectral-epitaph");
    const findingsList = document.getElementById("findings-list");

    rotNum.textContent = audit.bit_rot_score;
    statusText.textContent = audit.cemetery_status;
    yearsText.textContent = `~${audit.years_dormant} Years`;
    epitaphText.textContent = `"${audit.spectral_epitaph}"`;

    if (audit.bit_rot_score > 60) {
      rotCircle.className = "rot-circle rot-high";
    } else {
      rotCircle.className = "rot-circle rot-low";
    }

    findingsList.innerHTML = "";
    audit.findings.forEach(f => {
      const item = document.createElement("div");
      item.className = "finding-item";
      item.innerHTML = `
        <div class="finding-header">
          <strong>${f.title}</strong>
          <span class="sev-tag sev-${f.severity}">${f.severity}</span>
        </div>
        <div style="color: var(--text-muted); font-size: 0.75rem; margin-bottom: 0.25rem;">${f.description}</div>
        <div style="color: var(--ectoplasm-green); font-size: 0.75rem;">⚰️ <strong>Remedy:</strong> ${f.ghost_remedy}</div>
      `;
      findingsList.appendChild(item);
    });

    document.getElementById("audit-results-card").style.display = "block";
  }

  // Perform Resurrection
  btnResurrect?.addEventListener("click", async () => {
    btnResurrect.disabled = true;
    btnResurrect.textContent = "Chanting Ritual...";

    try {
      const resp = await fetch("/api/resurrect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repo_name: currentSample,
          files: [{ path: `${currentSample}.py`, content: codeArea.value, language: "python" }]
        })
      });

      const data = await resp.json();
      latestPlan = data.plan;
      renderResurrectionPlan(data.plan);
      renderTelemetrySpans(data.telemetry_spans);

      // Play bell chime
      window.spectralAudio.playResurrectionChime();

      // Switch to Modernization tab
      document.querySelector('[data-tab="altar-tab"]').click();
    } catch (err) {
      console.error("Resurrection error:", err);
      alert("Error casting resurrection ritual.");
    } finally {
      btnResurrect.disabled = false;
      btnResurrect.textContent = "⚡ Cast Resurrection Ritual";
    }
  });

  function renderResurrectionPlan(plan) {
    const diffContainer = document.getElementById("diff-container");
    const notesContainer = document.getElementById("notes-container");
    const testsContainer = document.getElementById("tests-container");

    diffContainer.innerHTML = "";
    notesContainer.innerHTML = "";

    plan.patches.forEach(p => {
      // Diff View
      const pre = document.createElement("pre");
      pre.className = "diff-view";
      
      const lines = p.unified_diff.split("\n");
      const formatted = lines.map(line => {
        if (line.startsWith("+") && !line.startsWith("+++")) {
          return `<span class="diff-add">${escapeHtml(line)}</span>`;
        } else if (line.startsWith("-") && !line.startsWith("---")) {
          return `<span class="diff-rem">${escapeHtml(line)}</span>`;
        }
        return escapeHtml(line);
      }).join("\n");

      pre.innerHTML = formatted;
      diffContainer.appendChild(pre);

      // Notes
      p.modernization_notes.forEach(note => {
        const li = document.createElement("li");
        li.textContent = note;
        li.style.fontSize = "0.85rem";
        li.style.marginBottom = "0.35rem";
        notesContainer.appendChild(li);
      });

      // Tests
      if (p.generated_tests) {
        testsContainer.textContent = p.generated_tests;
      }
    });

    document.getElementById("dockerfile-container").textContent = plan.dockerfile_modernized || "";
  }

  // Séance Chat
  const seanceInput = document.getElementById("seance-input");
  const seanceBtn = document.getElementById("seance-send-btn");
  const chatMessages = document.getElementById("chat-messages");
  const quickChips = document.querySelectorAll(".quick-chip");

  quickChips.forEach(chip => {
    chip.addEventListener("click", () => {
      seanceInput.value = chip.textContent;
      sendSeanceMessage();
    });
  });

  seanceBtn?.addEventListener("click", sendSeanceMessage);
  seanceInput?.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendSeanceMessage();
  });

  async function sendSeanceMessage() {
    const text = seanceInput.value.trim();
    if (!text) return;

    // User message
    appendChatMessage("user", text);
    seanceInput.value = "";

    seanceBtn.disabled = true;
    seanceBtn.textContent = "Summoning...";

    try {
      const resp = await fetch("/api/seance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repo_name: currentSample,
          message: text,
          history: chatHistory,
          findings_context: latestAudit ? latestAudit.spectral_epitaph : ""
        })
      });

      const data = await resp.json();
      appendChatMessage("ghost_maintainer", data.reply, data.spectral_mood);

      // Play spectral voice (ElevenLabs or Web Speech)
      window.spectralAudio.playSpectralVoice(data.reply, data.audio_base64);

      if (data.agent_spans) {
        renderTelemetrySpans(data.agent_spans);
      }
    } catch (err) {
      console.error("Séance error:", err);
      appendChatMessage("ghost_maintainer", "The connection to the spectral ether wavered... but I remain.", "mournful");
    } finally {
      seanceBtn.disabled = false;
      seanceBtn.textContent = "Summon";
    }
  }

  function appendChatMessage(role, content, mood = "") {
    chatHistory.push({ role, content, spectral_mood: mood });
    const div = document.createElement("div");
    div.className = `chat-msg ${role === 'user' ? 'msg-user' : 'msg-ghost'}`;
    
    if (role === 'ghost_maintainer') {
      div.innerHTML = `<span style="font-size:0.7rem; color:var(--spectral-purple); display:block; font-family:var(--font-mono); margin-bottom:0.25rem;">👻 Ghost Maintainer [${mood.toUpperCase() || 'SPIRIT'}]</span>${escapeHtml(content)}`;
    } else {
      div.textContent = content;
    }

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Telemetry Inspector
  function renderTelemetrySpans(spans) {
    const list = document.getElementById("telemetry-span-list");
    if (!list || !spans || !spans.length) return;

    list.innerHTML = "";
    spans.forEach(s => {
      const card = document.createElement("div");
      card.className = `span-card ${s.status === 'error' ? 'span-error' : ''}`;
      card.innerHTML = `
        <span class="span-time">${s.duration_ms}ms</span>
        <div style="font-weight:bold; color:var(--spectral-purple);">${escapeHtml(s.op)}</div>
        <div style="color:var(--text-muted); font-size:0.7rem;">${escapeHtml(s.description)}</div>
      `;
      list.appendChild(card);
    });
  }

  // Graveyard Vault loader
  async function loadGraveyardRecords() {
    const tbody = document.getElementById("graveyard-tbody");
    if (!tbody) return;

    try {
      const resp = await fetch("/api/graveyard");
      const records = await resp.json();
      tbody.innerHTML = "";

      records.forEach(r => {
        const tr = document.createElement("tr");
        const dateStr = new Date(r.created_at * 1000).toLocaleDateString();
        tr.innerHTML = `
          <td><strong>${escapeHtml(r.repo_name)}</strong></td>
          <td><span class="sev-tag ${r.bit_rot_score > 60 ? 'sev-CRITICAL' : 'sev-LOW'}">${r.bit_rot_score}/100</span></td>
          <td>${escapeHtml(r.cemetery_status)}</td>
          <td>${r.resurrected ? '<span style="color:var(--ectoplasm-green);">⚡ Resurrected</span>' : '<span style="color:var(--crypt-red);">⚰️ Buried</span>'}</td>
          <td style="color:var(--text-muted); font-size:0.75rem;">${escapeHtml(r.epitaph)}</td>
          <td>${dateStr}</td>
        `;
        tbody.appendChild(tr);
      });
    } catch (err) {
      console.warn("Could not load graveyard vault:", err);
    }
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
});
