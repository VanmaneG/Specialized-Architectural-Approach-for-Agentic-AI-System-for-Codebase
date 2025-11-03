from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """
    An abstract base class for defining agents.
    Provides a structured approach for agent initialization, execution, and finalization.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass
