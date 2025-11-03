from graph.pipeline_langgraph import build_graph
from graph.graph_state import GraphState
from core.logger import setup_logger

LOG = setup_logger(__name__)

if __name__ == "__main__":
    graph = build_graph()

    init_state = GraphState(
        new_spec="./data/specs/new_spec.txt",
        old_spec="./data/specs/old_spec.txt",
        summary_new_spec="",
        summary_old_spec="",
        diff_keywords={},
        candidate_files=[],
        plan=[],
        current_hypothesis={},
        branches=[],
        execution_results=[],
        evaluation_report={},
        needs_replan=False,
    )

    LOG.info("Starting LangGraph Agentic Pipeline...")
    final_state = graph.invoke(init_state)
    LOG.info("✅ Final Evaluation Report:")
    LOG.info(final_state.get("evaluation_report"))
