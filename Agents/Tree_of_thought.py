from core.base_agent import BaseAgent
from core.logger import setup_logger

LOG = setup_logger(__name__)

class TreeOfThoughtAgent(BaseAgent):
    def __init__(self):
        super().__init__("TreeOfThoughtAgent")

    def run(self, state):
        h = state.get("current_hypothesis", {})
        branches = [
            {"branch": "B1", "strategy": "modify_inplace"},
            {"branch": "B2", "strategy": "add_wrapper"},
        ]
        LOG.info(f"TreeOfThoughtAgent: branches {branches}")
        return {"branches": branches}
