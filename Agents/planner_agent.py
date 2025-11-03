from core.base_agent import BaseAgent
from core.logger import setup_logger
from agents.llm_reasoner import LLMReasoner

LOG = setup_logger(__name__)

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("PlannerAgent")
        self.hf = LLMReasoner()

    def run(self, state):
        # ensure rag_contexts exist
        out = self.hf.plan(state)
        # also synthesize a structured plan (simple parse)
        plan_text = out.get("plan_text", "")
        # placeholder: split into steps by newline
        steps = [{"step_no": i+1, "text": s.strip()} for i, s in enumerate(plan_text.split("\n")) if s.strip()]
        LOG.info("PlannerAgent: generated %d steps", len(steps))
        return {"plan": steps, "plan_text": plan_text}
