import asyncio
import logging
import random
from dataclasses import dataclass
from typing import Any

# ตั้งค่า Logger
logger = logging.getLogger("GENESIS_CORE")

@dataclass
class RAMConfig:
    max_concurrent_tasks: int = 5
    max_retries: int = 3
    retry_base_delay: float = 0.5

class RobustAsyncManager:
    """
    R.A.M. (Robust Async Manager) - The Heart of the System
    ทำหน้าที่บริหารจัดการ Task และความพร้อมกันของการทำงาน (Concurrency)
    """
    def __init__(self, config: RAMConfig = RAMConfig()):
        self.config = config
        self.semaphore = asyncio.Semaphore(config.max_concurrent_tasks)

    async def execute_task(self, task_name: str, workload_func: Any, *args):
        async with self.semaphore:
            # Mock Processing Logic
            logger.info(f"❤️ [R.A.M.] Pumping task: {task_name}")
            await asyncio.sleep(random.uniform(0.5, 1.5)) # Simulating work

            # Check for simulated critical failure logic based on rules
            if "INFINITE_LOOP" in task_name:
                raise ValueError("PARAJIKA_03 Triggered: Recursive Loop Detected")

            return f"✅ {task_name} Completed via R.A.M."
