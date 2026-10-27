"""
Unit tests for Spectral Code Auditor.
"""

import pytest
from app.models.schemas import FileEntry
from app.core.code_auditor import code_auditor

def test_audit_detects_legacy_python2_print_and_xrange():
    legacy_code = 'print "Deprecated print statement"\nfor i in xrange(10):\n    pass\n'
    files = [FileEntry(path="legacy.py", content=legacy_code)]
    
    result = code_auditor.audit_repository("LegacyTestRepo", files)
    
    assert result.bit_rot_score > 30
    assert result.total_files == 1
    
    categories = [f.category for f in result.findings]
    assert "deprecated_syntax" in categories
    assert any("xrange" in f.title.lower() for f in result.findings)

def test_audit_detects_md5_vulnerability():
    vuln_code = 'import hashlib\nh = hashlib.md5("secret".encode()).hexdigest()\n'
    files = [FileEntry(path="vuln.py", content=vuln_code)]
    
    result = code_auditor.audit_repository("CryptoTestRepo", files)
    
    severities = [f.severity for f in result.findings]
    assert "CRITICAL" in severities
    assert any("CVE-2004-2761" in f.description for f in result.findings)

def test_audit_clean_code_scores_low():
    clean_code = '''"""Modern python module."""
from typing import List

def calculate_sum(items: List[int]) -> int:
    return sum(items)
'''
    files = [FileEntry(path="clean.py", content=clean_code)]
    result = code_auditor.audit_repository("CleanRepo", files)
    
    assert result.bit_rot_score <= 15
    assert len(result.findings) == 0
