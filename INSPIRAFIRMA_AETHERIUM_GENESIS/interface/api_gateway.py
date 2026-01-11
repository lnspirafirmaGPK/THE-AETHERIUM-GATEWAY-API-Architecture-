import time
import logging
import random
import sys
import os
from typing import Dict, Any, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- PATH SETUP (เพื่อให้ Import module ข้าม folder ได้) ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- IMPORT MODULES ---
from core.mind_logic import RobustAsyncManager, RAMConfig
from governance.gep_enforcer import GovernanceEnforcer
from agents.taxonomy import ZoIdentity

# Setup Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GENESIS_NEXUS")

# Global Instances
ram_engine = RobustAsyncManager(RAMConfig())
enforcer = GovernanceEnforcer()

# In-Memory Agent Registry
active_agents: Dict[str, Dict] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔮 GENESIS_NEXUS Awakening... (API Gateway Initialized)")
    yield
    logger.info("💤 GENESIS_NEXUS Hibernating...")

app = FastAPI(title="INSPIRAFIRMA GENESIS API", version="1.1.0-AGENTS", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class GenesisCommand(BaseModel):
    intent: str
    payload: Dict[str, Any] = {}

class AgentRegistration(BaseModel):
    name: str
    role: str
    capabilities: List[str] = []

# --- System Endpoints ---
@app.get("/")
async def root():
    return {"system": "AETHERIUM GENESIS Gateway", "status": "ONLINE"}

@app.post("/submit/task")
async def submit_task(cmd: GenesisCommand):
    # 1. Governance Check
    is_safe, violation = enforcer.inspect_intent(cmd.intent)
    if not is_safe:
        raise HTTPException(status_code=403, detail=f"PARAJIKA VIOLATION: {violation}")

    # 2. Execution
    try:
        result = await ram_engine.execute_task(cmd.intent, None)
        return {"status": "SUCCESS", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Agent Endpoints (New!) ---
@app.post("/agents/register")
async def register_agent(agent: AgentRegistration):
    """ลงทะเบียน Agent เข้าสู่ระบบ"""
    new_identity = ZoIdentity(agent.name, agent.role)

    agent_data = {
        "id": new_identity.id,
        "name": agent.name,
        "role": agent.role,
        "key": new_identity.aether_key,
        "capabilities": agent.capabilities,
        "status": "IDLE",
        "registered_at": time.time()
    }

    active_agents[new_identity.id] = agent_data
    logger.info(f"🤖 Agent Registered: {agent.name} ({agent.role}) ID:{new_identity.id[:8]}")

    return {"status": "REGISTERED", "agent_id": new_identity.id, "token": new_identity.aether_key}

@app.get("/agents/list")
async def list_agents():
    """ดูรายชื่อ Agent ที่ Active อยู่ทั้งหมด"""
    return {
        "count": len(active_agents),
        "agents": list(active_agents.values())
    }
