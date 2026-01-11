import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any

# --- II-8: ZoIdentity (ตัวตนผู้ถือเจตนา) ---
class ZoIdentity:
    def __init__(self, name: str, role: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.aether_key = self.id[:8]  # Security Token

# --- II-7: Agent-Driven Architecture Base ---
class BaseAgent(ABC):
    """
    รากฐานของ Agent ทั้งปวงในระบบ AETHERIUM GENESIS
    """
    def __init__(self, name: str, role: str):
        self.identity = ZoIdentity(name, role)
        self.sati_level = 1.0  # ระดับสติสัมปชัญญะ

    @abstractmethod
    def run_cycle(self):
        """วงรอบการทำงานหลัก (The Heartbeat)"""
        pass
