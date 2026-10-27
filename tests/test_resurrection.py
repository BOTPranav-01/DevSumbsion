"""
Unit tests for Resurrection Engine.
"""

import pytest
from app.models.schemas import FileEntry
from app.core.resurrection import resurrection_engine

def test_resurrection_modernizes_python2_and_hashes():
    legacy_code = 'print "Modernizing..."\nh = hashlib.md5("token")\nfor i in xrange(5):\n    pass\n'
    files = [FileEntry(path="old_app.py", content=legacy_code)]

    plan = resurrection_engine.resurrect_codebase("OldApp", files)

    assert plan.success is True
    assert len(plan.patches) == 1

    patch = plan.patches[0]
    assert 'print("Modernizing...")' in patch.resurrected_code
    assert "hashlib.sha256(" in patch.resurrected_code
    assert "range(5)" in patch.resurrected_code
    assert len(patch.modernization_notes) >= 3
    assert "diff" in patch.unified_diff.lower() or "---" in patch.unified_diff

def test_resurrection_generates_pytest_suite_and_dockerfile():
    code = "def sample():\n    return 42\n"
    files = [FileEntry(path="sample.py", content=code)]

    plan = resurrection_engine.resurrect_codebase("SampleRepo", files)

    assert plan.dockerfile_modernized is not None
    assert "FROM python:3.12-slim" in plan.dockerfile_modernized
    assert plan.ci_cd_workflow is not None
    assert "pytest tests/" in plan.ci_cd_workflow
