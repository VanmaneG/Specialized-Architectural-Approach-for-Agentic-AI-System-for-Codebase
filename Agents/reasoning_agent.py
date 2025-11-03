from core.base_agent import BaseAgent
from core.logger import setup_logger
from agents.llm_reasoner import LLMReasoner

LOG = setup_logger(__name__)

class ReActAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReActAgent")
        self.hf = LLMReasoner()

    def run(self, state):
        # ask the LLM for a next-action given plan + contexts
        out = self.hf.react(state)
        react_text = out.get("react_text", "")
        # try to identify next action token (edit/run/retrieve)
        action = "edit_code" if "edit" in react_text.lower() or "modify" in react_text.lower() else "run_tests"
        LOG.info("ReActAgent: decided action=%s", action)
        return {"current_react": {"action": action, "rationale": react_text}}
