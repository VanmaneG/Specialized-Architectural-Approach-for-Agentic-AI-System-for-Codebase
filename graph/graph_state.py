from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict, total=False):
    new_spec: str
    old_spec: str
    summary_new_spec: str
    summary_old_spec: str
    diff_keywords: Dict[str, List[str]]
    candidate_files: List[str]
    plan: List[Dict[str, Any]]
    current_hypothesis: Dict[str, Any]
    branches: List[Dict[str, Any]]
    execution_results: List[Dict[str, Any]]
    evaluation_report: Dict[str, Any]
    needs_replan: bool


