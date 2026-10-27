"""
Graveyard Vault for NecroCode.
Integrates with MongoDB Atlas for persistent storage of ghost repository audits,
epitaphs, and resurrection logs, with an automatic in-memory fallback.
"""

import time
import logging
from typing import List, Dict, Any, Optional
from app.config import settings
from app.models.schemas import GraveyardRecord

logger = logging.getLogger("necrocode.vault")

class GraveyardVault:
    def __init__(self):
        self.mongo_client = None
        self.db = None
        self.collection = None
        self._in_memory_records: List[Dict[str, Any]] = [
            {
                "id": "grave-1",
                "repo_name": "py-crypto-legacy (1998)",
                "bit_rot_score": 92,
                "cemetery_status": "Decomposed Zombie",
                "created_at": time.time() - 86400 * 5,
                "epitaph": "Haunted by broken MD5 collision digests and unbuffered raw sockets.",
                "resurrected": True
            },
            {
                "id": "grave-2",
                "repo_name": "phantom-worker-threads (2015)",
                "bit_rot_score": 78,
                "cemetery_status": "Haunted Legacy",
                "created_at": time.time() - 86400 * 2,
                "epitaph": "Killed by silent deadlocks and zombie daemon threads holding locks eternally.",
                "resurrected": True
            },
            {
                "id": "grave-3",
                "repo_name": "abandoned-scraper-2016",
                "bit_rot_score": 64,
                "cemetery_status": "Restless Spirit",
                "created_at": time.time() - 86400 * 1,
                "epitaph": "Stranded in Python 2 urllib2 purgatory after maintainer graduated university.",
                "resurrected": False
            }
        ]
        self._init_mongodb()

    def _init_mongodb(self):
        if settings.mongodb_uri:
            try:
                from pymongo import MongoClient
                self.mongo_client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)
                self.db = self.mongo_client[settings.mongodb_database]
                self.collection = self.db["graveyard_records"]
                logger.info("Connected to MongoDB Atlas Graveyard Vault successfully.")
            except Exception as e:
                logger.warning(f"MongoDB Atlas initialization failed ({e}), using in-memory vault.")
                self.collection = None

    def store_record(self, record: GraveyardRecord) -> bool:
        doc = record.model_dump()
        if self.collection is not None:
            try:
                self.collection.update_one({"id": record.id}, {"$set": doc}, upsert=True)
                return True
            except Exception as e:
                logger.warning(f"MongoDB write error ({e}), storing in memory.")
        
        # In-memory storage
        self._in_memory_records = [r for r in self._in_memory_records if r["id"] != record.id]
        self._in_memory_records.insert(0, doc)
        return True

    def get_all_records(self) -> List[Dict[str, Any]]:
        if self.collection is not None:
            try:
                records = list(self.collection.find({}, {"_id": 0}).sort("created_at", -1))
                if records:
                    return records
            except Exception as e:
                logger.warning(f"MongoDB read error ({e}), returning memory records.")
        return self._in_memory_records

graveyard_vault = GraveyardVault()
