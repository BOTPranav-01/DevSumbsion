"""
Sentry Agent Tracing & Observability integration.
Supports Sentry's AI Agent Tracing for monitoring open-source AI agent loops,
reasoning steps, tool executions, and LLM generations.
"""

import time
import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

from app.config import settings

logger = logging.getLogger("necrocode.telemetry")

_sentry_initialized = False

def init_sentry():
    global _sentry_initialized
    if settings.sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.fastapi import FastApiIntegration
            
            sentry_sdk.init(
                dsn=settings.sentry_dsn,
                traces_sample_rate=settings.sentry_traces_sample_rate,
                integrations=[FastApiIntegration()],
                release=f"necrocode@{settings.app_version}",
                environment="production" if settings.is_render else "development"
            )
            _sentry_initialized = True
            logger.info("Sentry Agent Tracing initialized successfully.")
        except Exception as e:
            logger.warning(f"Failed to initialize Sentry: {e}")
    else:
        logger.info("Sentry DSN not configured; running with internal in-memory Agent Tracing.")

class AgentSpanRecorder:
    """Records traces for agentic execution steps to be visualized in UI or dispatched to Sentry."""
    def __init__(self):
        self.spans: List[Dict[str, Any]] = []

    def start_span(self, op: str, description: str, data: Optional[Dict[str, Any]] = None):
        span_id = f"span_{len(self.spans) + 1}_{int(time.time() * 1000)}"
        span_record = {
            "span_id": span_id,
            "op": op,
            "description": description,
            "start_time": time.time(),
            "status": "running",
            "data": data or {},
            "duration_ms": 0
        }
        self.spans.append(span_record)
        return span_id

    def finish_span(self, span_id: str, status: str = "ok", extra_data: Optional[Dict[str, Any]] = None):
        for s in self.spans:
            if s["span_id"] == span_id:
                s["status"] = status
                s["end_time"] = time.time()
                s["duration_ms"] = round((s["end_time"] - s["start_time"]) * 1000, 2)
                if extra_data:
                    s["data"].update(extra_data)
                break

@contextmanager
def trace_agent_step(op: str, description: str, recorder: Optional[AgentSpanRecorder] = None, data: Optional[Dict[str, Any]] = None):
    """Context manager for tracing agent execution steps with Sentry and internal telemetry."""
    span_id = None
    if recorder:
        span_id = recorder.start_span(op, description, data)
    
    sentry_span = None
    if _sentry_initialized:
        try:
            import sentry_sdk
            sentry_span = sentry_sdk.start_span(op=op, description=description)
            sentry_span.__enter__()
            if data:
                for k, v in data.items():
                    sentry_sdk.set_extra(k, v)
        except Exception as e:
            logger.debug(f"Sentry span error: {e}")

    try:
        yield span_id
        if recorder and span_id:
            recorder.finish_span(span_id, "ok")
    except Exception as exc:
        if recorder and span_id:
            recorder.finish_span(span_id, "error", {"error": str(exc)})
        if _sentry_initialized:
            try:
                import sentry_sdk
                sentry_sdk.capture_exception(exc)
            except Exception:
                pass
        raise
    finally:
        if sentry_span:
            try:
                sentry_span.__exit__(None, None, None)
            except Exception:
                pass
