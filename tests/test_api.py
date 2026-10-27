"""
Integration tests for FastAPI server endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["app"] == "NecroCode"

def test_samples_endpoint():
    resp = client.get("/api/samples")
    assert resp.status_code == 200
    samples = resp.json()
    assert len(samples) >= 3
    sample_ids = [s["id"] for s in samples]
    assert "legacy_crypto" in sample_ids

def test_audit_api_endpoint():
    payload = {
        "repo_name": "TestApiRepo",
        "preset_sample": "legacy_crypto"
    }
    resp = client.post("/api/audit", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "audit" in data
    assert data["audit"]["bit_rot_score"] > 50

def test_resurrect_api_endpoint():
    payload = {
        "repo_name": "TestApiRepo",
        "preset_sample": "legacy_crypto"
    }
    resp = client.post("/api/resurrect", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "plan" in data
    assert len(data["plan"]["patches"]) > 0

def test_seance_api_endpoint():
    payload = {
        "repo_name": "TestApiRepo",
        "message": "Who are you?"
    }
    resp = client.post("/api/seance", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data
    assert len(data["reply"]) > 10

def test_graveyard_api_endpoint():
    resp = client.get("/api/graveyard")
    assert resp.status_code == 200
    records = resp.json()
    assert isinstance(records, list)
    assert len(records) > 0
