import json
import logging
import os
from typing import Tuple, Optional

logger = logging.getLogger("GENESIS_GOV")

class GovernanceEnforcer:
    """
    GEP Enforcer (Governance Enforcement Protocol)
    ผู้ตรวจสอบความถูกต้องตามกฎระเบียบ (Patimokkha/Inspirafirma Ruleset)
    """
    def __init__(self, ruleset_path: str = "governance/inspirafirma_ruleset.json"):
        # ปรับ Path ให้ยืดหยุ่น (รองรับการรันจาก Root หรือ Subfolder)
        base_path = os.path.dirname(os.path.abspath(__file__))
        # ถ้าหาไฟล์ใน path ที่ระบุไม่เจอ ให้ลองหาใน folder เดียวกับ script นี้
        if not os.path.exists(ruleset_path):
             self.ruleset_path = os.path.join(base_path, "inspirafirma_ruleset.json")
        else:
             self.ruleset_path = ruleset_path

        self.rules = self._load_rules()
        self.violation_count = 0

    def _load_rules(self):
        try:
            with open(self.ruleset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"📜 Governance Loaded: {data.get('meta', {}).get('project', 'Unknown')} Ruleset")
                return data
        except FileNotFoundError:
            logger.warning(f"⚠️ Ruleset file not found at {self.ruleset_path}! Using Default Fallback.")
            return {"prime_directives": []}

    def inspect_intent(self, intent: str) -> Tuple[bool, Optional[str]]:
        """
        ตรวจสอบเจตนา (Intent) ว่าขัดต่อ PARAJIKA หรือไม่
        """
        directives = self.rules.get("prime_directives", [])

        for rule in directives:
            forbidden_keywords = rule.get('keywords', [])
            for keyword in forbidden_keywords:
                if keyword in intent.lower():
                    logger.critical(f"🛑 BLOCKED by {rule['id']}: {rule['name']}")
                    self.violation_count += 1
                    return False, rule['id']

        return True, None
