# agents/llm_reasoner.py
from core.base_agent import BaseAgent
from core.logger import setup_logger
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os

LOG = setup_logger(__name__)

HF_MODEL = os.environ.get("HF_MODEL", "######")  # choose based on resource
USE_HF_HUB = os.environ.get("USE_HF_HUB", "false").lower() == "true"

class LLMReasoner(BaseAgent):
    def __init__(self, model_name: str = HF_MODEL):
        super().__init__("LLMReasoner")
        # create a text-generation pipeline
        # For causal LMs:
        try:
            # If using a causal LM, change pipeline accordingly
            self.generator = pipeline("text2text-generation", model=model_name, device=0 if os.environ.get("CUDA_VISIBLE_DEVICES") else -1)
            LOG.info("LLMReasoner: initialized HF model %s", model_name)
        except Exception as e:
            LOG.warning("LLMReasoner: failed to initialize model %s (%s). Using simple fallback.", model_name, str(e))
            self.generator = None

    def generate(self, prompt: str, max_length: int = 512):
        if self.generator:
            out = self.generator(prompt, max_length=max_length, do_sample=False)
            if isinstance(out, list) and out:
                text = out[0].get("generated_text") or out[0].get("summary_text") or out[0].get("text")
                return text
        # fallback simple echo
        LOG.warning("LLMReasoner: falling back to echo for prompt")
        return "FALLBACK: " + prompt[:500]

    def plan(self, state):
        # create planner prompt from rag_contexts and diff keywords
        diff = state.get("diff_keywords", {})
        contexts = state.get("rag_contexts", [])
        ctx_text = "\n".join([c["text"] for c in contexts])
        prompt = f"""You are an engineer. New spec diffs: {diff}. Context:\n{ctx_text}\nCreate a step-by-step plan to implement the changes (concise)."""
        out = self.generate(prompt)
        return {"plan_text": out}

    def react(self, state):
        # ReAct-style single-step reasoning and decide action
        plan_text = state.get("plan_text", "")
        prompt = f"""Given the plan: {plan_text}\nSuggest the next best action and a short rationale."""
        out = self.generate(prompt)
        return {"react_text": out}
