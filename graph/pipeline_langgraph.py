from langgraph.graph import StateGraph, END
from graph.graph_state import GraphState

from agents.context_synthesizer import ContextSynthesizer
from agents.goal_retriever import GoalRetriever
from agents.planner_agent import PlannerAgent
from agents.reasoning_agent import ReActAgent
from agents.tree_of_thought_agent import TreeOfThoughtAgent
from agents.action_executor import ExecutorAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.failure_detector import FailureDetector
from agents.report_agent import ReportAgent

# Instantiate agents
ctx = ContextSynthesizer()
diff = GoalRetriever()
ctx_rag = ContextCuratorRAG()
planner = PlannerAgent()
react = ReActAgent()
tot = TreeOfThoughtAgent()
executor = ExecutorAgent()
evaluator = EvaluatorAgent()
failure = FailureDetector()
report = ReportAgent()


# Node functions
def node_context(state: GraphState) -> GraphState:
    return ctx.run(state)

def node_diff(state: GraphState) -> GraphState:
    return diff.run(state)

def node_planner(state: GraphState) -> GraphState:
    return planner.run(state)

def node_react(state: GraphState) -> GraphState:
    return react.run(state)

def node_tot(state: GraphState) -> GraphState:
    return tot.run(state)

def node_executor(state: GraphState) -> GraphState:
    return executor.run(state)

def node_eval(state: GraphState) -> GraphState:
    return evaluator.run(state)

def node_failure(state: GraphState) -> GraphState:
    return failure.run(state)

def node_report(state: GraphState) -> GraphState:
    return report.run(state)

# Build the graph
def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("context", node_context)
    builder.add_node("diff", node_diff)
    builder.add_node("planner", node_planner)
    builder.add_node("react", node_react)
    builder.add_node("tot", node_tot)
    builder.add_node("executor", node_executor)
    builder.add_node("eval", node_eval)
    builder.add_node("failure", node_failure)
    builder.add_node("report", node_report)

    # Set entry point
    builder.set_entry_point("context")

    # Sequential edges
    builder.add_edge("context", "diff")
    builder.add_edge("diff", "planner")
    builder.add_edge("planner", "react")
    builder.add_edge("react", "tot")
    builder.add_edge("tot", "executor")
    builder.add_edge("executor", "eval")
    builder.add_edge("eval", "failure")
    # nodes
    builder.add_node("context_rag", lambda s: ctx_rag.run(s))
    # then planner, react, tot, executor, eval, failure...
    builder.add_edge("context_rag", "planner")

    # Conditional edge: loop back if replanning is needed
    builder.add_conditional_edges(
        "failure",
        lambda state: "planner" if state.get("needs_replan", False) else "report"
    )

    builder.add_edge("report", END)
    return builder.compile()

