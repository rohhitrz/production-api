"""
Response Caching Layer
In-memory cache with TTL for LLM response deduplication.

"""

import hashlib
import time
from typing import Optional

class ResponseCache:
    """
    In-memory response cache with TTL (time-to-live).

    In production, replace this with Redis for:
    - Persistence across restarts
    - Shared cache across multiple instances
    - Built-in TTL management
    """


    def __init__(self, ttl_seconds: int=300):
        self.ttl=ttl_seconds
        self._cache:dict[str, dict]={}
        self._hits=0
        self._misses=0
    

    def _make_key(self, query:str)->str:
        """create a cached key from normalized query."""
        normalized=query.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    # 'What is Python?' and 'what is python?'

    def get(self, query: str) -> Optional[str]:
        """
        Get cached response if it exists and hasn't expired.
        Returns None on cache miss.
        """
        key = self._make_key(query)

        if key in self._cache:
            entry = self._cache[key]
            # Check TTL
            if time.time() - entry["timestamp"] < self.ttl:
                self._hits += 1
                return entry["response"]
            else:
                # Expired - remove it
                del self._cache[key]

        self._misses += 1
        return None

