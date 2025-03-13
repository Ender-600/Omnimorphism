import os
import unittest
from omnimorph.agents.agent_workflow import app, AgentState

def run_workflow() -> AgentState:
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
    return result

def run_unit_tests():
    tests_dir = os.path.join(os.path.dirname(__file__), "..", "tests")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=tests_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        raise Exception("Some unit tests failed.")
    print("All unit tests passed.")

def compile_agent_main():
    print("=== Starting Compile Agent ===")
    
    state_result = run_workflow()
    print("Workflow Result:")
    print("Generated Code:")
    print(state_result["code_solution"])
    print("Test Results:")
    print(state_result["test_results"])
    if state_result["errors"]:
        print("Errors:", state_result["errors"])
        raise Exception("Workflow did not complete successfully.")
    
    run_unit_tests()
    
    print("=== Compile Agent Finished Successfully ===")

if __name__ == "__main__":
    compile_agent_main()
