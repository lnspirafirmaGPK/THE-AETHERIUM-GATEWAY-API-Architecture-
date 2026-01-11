import json
import time
import logging
from typing import Dict, Any
from agents.taxonomy import BaseAgent

# ตั้งค่า Logging ตามมาตรฐานสากล
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PangenesAgent")

class PangenesAgent(BaseAgent):
    """
    PangenesAgent: Responsible for Recursive Self-Improvement (RSI) logic.
    Analyzes system errors and records insights for autonomous optimization.
    """
    def __init__(self):
        # ปรับการเรียก super() ให้ตรงกับโครงสร้าง BaseAgent
        super().__init__("Pangenes", "Architect")
        self.knowledge_base_path = "core/system_insights.jsonl"
        self.optimization_level = 1.0 

    def trigger_self_correction(self, error_report: Dict[str, Any]):
        """
        Processes system error reports and generates optimization insights.
        """
        logger.info(f"Processing error report: {error_report.get('error_type')}")
        
        # 1. Error Analysis and Insight Generation
        insight_data = {
            "timestamp": time.time(),
            "agent_id": self.identity.id, # อ้างอิงจาก ZoIdentity
            "source": error_report.get("source"),
            "resolution_hint": f"Optimization logic for {error_report.get('task_name')}",
            "improvement_increment": 0.01 
        }

        # 2. Persist to Knowledge Base
        self._store_insight(insight_data)
        
    def _store_insight(self, data: Dict[str, Any]):
        """
        Appends analysis results to the system knowledge base (JSONL format).
        """
        try:
            with open(self.knowledge_base_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
            logger.info("Successfully recorded optimization insight.")
        except IOError as e:
            logger.error(f"File system error: Failed to record insight. Details: {e}")

    def run_cycle(self):
        """
        Main operational loop for proactive system health scanning.
        """
        logger.info("Scanning system components for potential optimizations...")
        # Future Logic: Implement automated health checks here.