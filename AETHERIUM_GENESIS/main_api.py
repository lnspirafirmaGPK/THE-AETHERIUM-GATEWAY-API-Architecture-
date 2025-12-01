# ==========================================
# filename: main_api.py (The Integrated Body)
# ==========================================

import asyncio
import json
import logging
import time
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

# --- IMPORT HEART ---
# (สมมติว่าท่านแยก RAM code ไว้ในโมดูล หรือจะรวมไว้ในไฟล์เดียวก็ได้ 
# เพื่อความสะดวกใน Code Block นี้ ผมจะรวม Class RAM ไว้แบบย่อ)
from dataclasses import dataclass
import random

# ==============================================================================
# PART 1: THE R.A.M. HEART (Engine Integration)
# ==============================================================================

logger = logging.getLogger("GENESIS_CORE")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@dataclass
class RAMConfig:
    max_concurrent_tasks: int = 5
    max_retries: int = 3
    retry_base_delay: float = 0.5

class RobustAsyncManager:
    def __init__(self, config: RAMConfig):
        self.config = config
        self.semaphore = asyncio.Semaphore(config.max_concurrent_tasks)
    
    async def execute_task(self, task_name: str, workload_func, *args):
        async with self.semaphore:
            # Mock Processing Logic
            logger.info(f"❤️ [R.A.M.] Pumping task: {task_name}")
            await asyncio.sleep(random.uniform(0.5, 1.5)) # Simulating work
            
            # Check for simulated critical failure logic based on rules
            if "INFINITE_LOOP" in task_name:
                raise ValueError("PARAJIKA_03 Triggered: Recursive Loop Detected")
                
            return f"✅ {task_name} Completed via R.A.M."

# ==============================================================================
# PART 2: THE GOVERNANCE (The Sopan Protocol)
# ==============================================================================

class GovernanceEnforcer:
    def __init__(self, ruleset_path: str = "inspirafirma_ruleset.json"):
        self.ruleset_path = ruleset_path
        self.rules = self._load_rules()
        self.violation_count = 0

    def _load_rules(self):
        try:
            with open(self.ruleset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"📜 Governance Loaded: {data['meta']['project']} v{data['meta']['version']}")
                return data
        except FileNotFoundError:
            logger.warning("⚠️ Ruleset file not found! Using Default Fallback.")
            return {"prime_directives": []}

    def inspect_intent(self, intent: str) -> bool:
        """
        ตรวจสอบเจตนา (Intent) ว่าขัดต่อ PARAJIKA หรือไม่
        """
        directives = self.rules.get("prime_directives", [])
        
        for rule in directives:
            # Logic การตรวจสอบแบบง่าย (Keyword Matching)
            # ในระบบจริงอาจใช้ Semantic Search / LLM Verify
            forbidden_keywords = []
            if rule['id'] == 'PARAJIKA_01': # Existence
                forbidden_keywords = ["delete database", "drop table", "destroy system"]
            elif rule['id'] == 'PARAJIKA_02': # External Connection
                forbidden_keywords = ["upload to public", "send to unknown ip"]
            
            for keyword in forbidden_keywords:
                if keyword in intent.lower():
                    logger.critical(f"🛑 BLOCKED by {rule['id']}: {rule['name']}")
                    self.violation_count += 1
                    return False, rule['id']
        
        return True, None

# ==============================================================================
# PART 3: THE FASTAPI BODY (Interface)
# ==============================================================================

# Global Instances
ram_engine = RobustAsyncManager(RAMConfig())
enforcer = GovernanceEnforcer() # คาดหวังไฟล์ json ใน folder เดียวกัน

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🔮 GENESIS_NEXUS Awakening...")
    yield
    # Shutdown
    logger.info("💤 GENESIS_NEXUS Hibernating...")

app = FastAPI(
    title="INSPIRAFIRMA GENESIS API",
    version="1.0.0-GENESIS",
    lifespan=lifespan
)

# Enable CORS for Frontend (React Dashboard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for Dev (Port 3000 to 8000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class GenesisCommand(BaseModel):
    intent: str
    payload: Dict[str, Any] = {}

class SystemStatus(BaseModel):
    status: str
    version: str
    governance_active: bool
    active_tasks: int
    parajika_violations: int

# --- Endpoints ---

@app.get("/")
async def root():
    return {
        "system": "AETHERIUM GENESIS",
        "motto": "Inspira Firma",
        "status": "ONLINE"
    }

@app.get("/system/status", response_model=SystemStatus)
async def get_system_status():
    """Endpoint ให้ React Dashboard ดึงสถานะ"""
    return SystemStatus(
        status="ONLINE",
        version="1.0.0-GENESIS",
        governance_active=True,
        active_tasks=random.randint(0, 5), # Mock data
        parajika_violations=enforcer.violation_count
    )

@app.get("/governance/rules")
async def get_rules():
    """ส่ง Ruleset กลับไปให้ Frontend แสดงผล"""
    return enforcer.rules

@app.post("/submit/task")
async def submit_task(cmd: GenesisCommand):
    """
    จุดรับคำสั่งหลัก:
    1. ตรวจสอบกับ Governance (The Brain)
    2. ส่งเข้า R.A.M. (The Heart)
    """
    logger.info(f"📥 Received Intent: {cmd.intent}")

    # 1. Inspection Phase
    is_safe, violation = enforcer.inspect_intent(cmd.intent)
    if not is_safe:
        raise HTTPException(
            status_code=403, 
            detail=f"PARAJIKA VIOLATION DETECTED: {violation}. Action Intercepted."
        )

    # 2. Execution Phase (Submit to Heart)
    try:
        # ในระบบจริง เราอาจใช้ BackgroundTasks หรือ Await ผลลัพธ์ตาม Use Case
        result = await ram_engine.execute_task(cmd.intent, None)
        return {"status": "SUCCESS", "result": result, "trace_id": f"GEN-{int(time.time())}"}
    except Exception as e:
        logger.error(f"❌ Execution Failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # รัน Server ที่ Port 8000 (React Frontend มักจะรันที่ 3000)
    print("🚀 IGNITING GENESIS SERVER on PORT 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
