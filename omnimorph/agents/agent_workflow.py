from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from pydantic import BaseModel, Field
import time

from omnimorph.agents.solution_generation import solution_generator


class AgentState(TypedDict):
    prompt: str
    code_solution: str  # the generated code as a string
    test_results: List[str]
    errors: List[str]

def generate_code(state: AgentState) -> AgentState:
    solution = solution_generator(state['prompt'])
    state['code_solution'] = solution.code  #  might later combine imports + code
    return state

def execute_tests(state: AgentState) -> AgentState:
    main_code = state.get("code_solution", "")
    tests_code = state.get("tests_code", "")
    try:
        exec_globals = {}
        exec(main_code, exec_globals)
        exec(tests_code, exec_globals)
        state['test_results'] = ["All tests passed."]
        state['errors'] = []
    except Exception as e:
        state['errors'] = [str(e)]
    return state


def refine_code(state: AgentState) -> AgentState:
    if state['errors']:
        refined_prompt = f"""
            The generated code produced the following errors: {state['errors']}.
            Please revise the code to address these errors.
            Original prompt:
            {state['prompt']}
            """
        solution = solution_generator(refined_prompt)
        state['code_solution'] = solution.code
    return state

# Build the workflow using LangGraph's StateGraph.
workflow = StateGraph(AgentState)
workflow.add_node("generate", generate_code)
workflow.add_node("test", execute_tests)
workflow.add_node("refine", refine_code)

workflow.add_edge(START, "generate")
workflow.add_edge("generate", "test")
workflow.add_edge("test", "refine")
workflow.add_edge("refine", "test")
workflow.add_edge("test", END, condition=lambda state: not state['errors'])

app = workflow.compile()

if __name__ == "__main__":
    initial_prompt = (
        "Write a Python function named 'fibonacci' that computes the Fibonacci sequence up to n. "
        "Include all necessary import statements and comprehensive unit tests."
    )
    initial_state: AgentState = {
        "prompt": initial_prompt,
        "code_solution": "",
        "test_results": [],
        "errors": []
    }
    result = app.invoke(initial_state)
    print("Final Generated Code:")
    print(result["code_solution"])
    print("Test Results:", result["test_results"])
    if result["errors"]:
        print("Errors:", result["errors"])
