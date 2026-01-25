
import time
from dataclasses import dataclass
from typing import Dict

from fastapi import HTTPException



@dataclass
class WindowCounter:
    window_start: float
    count: int



class InMemoryRateLimiter:
    """
    Rate limiter en memoria por key con ventana fija.
    MVP: se resetea al reiniciar el proceso
    """

    def __init__(self, max_requests: int, window_seconds: int, time_fn=time.time):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._time_fn = time_fn
        self._counters: Dict[str, WindowCounter] = {}

    
    def check(self, key:str) -> None:
        now = self._time_fn()
        c = self._counters.get(key)

        if c is None or (now - c.window_start) >= self.window_seconds: 
            self._counters[key] = WindowCounter(window_start=now, count=1)
            return
    
        c.count += 1
        if c.count > self.max_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")


    def reset(self) -> None:
        """Resetea contadores (útil para tests)"""
        self._counters.clear()
    