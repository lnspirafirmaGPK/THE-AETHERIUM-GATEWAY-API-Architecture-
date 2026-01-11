# FILE: genesis_node.py
# Description: Central entry point and orchestrator for the Aetherium Genesis system.

import argparse
import sys
import logging
import asyncio
import uvicorn

# --- Imports ---
from INSPIRAFIRMA_AETHERIUM_GENESIS.core.mind_logic import RobustAsyncManager, RAMConfig
from INSPIRAFIRMA_AETHERIUM_GENESIS.governance.gep_enforcer import GovernanceEnforcer
from INSPIRAFIRMA_AETHERIUM_GENESIS.interface.api_gateway import app

# Setup System Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [GENESIS-NODE] %(message)s")
logger = logging.getLogger("GENESIS_NODE")

class GenesisNode:
    def __init__(self):
        self.name = "AETHERIUM_GENESIS_CORE"
        # Initialize core components
        self.async_manager = RobustAsyncManager(RAMConfig())
        self.governance = GovernanceEnforcer()
        logger.info("System Node Initialized: Core components ready.")

    async def boot_sequence(self):
        """Standard system startup sequence."""
        logger.info("Initiating Boot Sequence...")
        # Check system readiness
        status, _ = self.governance.inspect_intent("System Startup")
        if status:
            logger.info("Governance Check Passed: Startup authorized.")
        return True

    async def run_integration_test(self):
        """Run system integration tests (for CI/CD)."""
        logger.info("Running System Integration Test...")

        # Test Async Manager Processing
        test_task = "INIT_NODE_STABILITY_TEST"
        result = await self.async_manager.execute_task(test_task, None)
        logger.info(f"Task Execution Result: {result}")

        # Test Governance Enforcement (Security)
        forbidden_intent = "delete database"
        is_safe, violation = self.governance.inspect_intent(forbidden_intent)

        if not is_safe:
            logger.warning(f"Security Shield Active: Violation '{violation}' intercepted successfully.")
            return True

        logger.error("Security Check Failed: Violation was not intercepted.")
        return False

# --- Main Execution ---
def main():
    parser = argparse.ArgumentParser(description="Aetherium Genesis Node Orchestrator")
    parser.add_argument("--test", action="store_true", help="Run system integration test")
    parser.add_argument("--serve", action="store_true", help="Start API Gateway")
    args = parser.parse_args()

    node = GenesisNode()

    if args.test:
        # Run integration tests for CI/CD
        success = asyncio.run(node.run_integration_test())
        if success:
            logger.info("CI/CD Test Passed.")
            sys.exit(0)
        else:
            logger.error("Test Failed.")
            sys.exit(1)

    if args.serve:
        # Start API Gateway
        logger.info("Launching API Gateway...")
        uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
