"""
Unit tests for Concurrency Heisenbug and Ghost Detection.
"""

import pytest
from app.models.schemas import FileEntry
from app.core.code_auditor import code_auditor

def test_detects_unsynchronized_shared_state():
    race_code = """
import threading

class Worker:
    def __init__(self):
        self.counter = 0
    def increment(self):
        self.counter += 1
"""
    files = [FileEntry(path="race.py", content=race_code)]
    result = code_auditor.audit_repository("RaceRepo", files)

    categories = [f.category for f in result.findings]
    assert "heisenbug_race_condition" in categories
    assert any("threading.Lock()" in f.ghost_remedy for f in result.findings)
