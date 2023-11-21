from ast import List
from typing import Any, Dict, Protocol


class ToolExecutor(Protocol):
    """This class defines the interface for the tool executor. 
    Every tool created for the agent should should also implement an interface like this.
    """
    def run(self, function_name: str, **parameters: Dict[str, Any]) -> Any:
        """This method should be implemented by the tool. 
        It should contain the logic to run the tool.
        """
        raise NotImplementedError
    
    @staticmethod
    def support(function_name: str) -> bool:
        """This method should be implemented by the tool. 
        It should return True if the tool supports the given function_name.
        """
        raise NotImplementedError


class FunctionExecutor:
    def __init__(self, tool_executors: List[ToolExecutor]):
        self.tool_executors = tool_executors

    def execute(self, function_name: str, **kwargs):
        for exec in self.tool_executors:
            if exec.support(function_name):
                return exec.run(function_name, **kwargs)
        
        return f"Unknown function {function_name} was called."