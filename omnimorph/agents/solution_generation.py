import os
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser



class CodeSolution(BaseModel):
    prefix: str = Field(description="Explanation of the problem and proposed solution")
    imports: str = Field(description="All required import statements")
    code: str = Field(description="The primary Python code implementation, which may include function definitions, conversion logic, or data integration routines.")
    tests: str = Field(description="Unit test code to validate the solution")


llm = ChatOpenAI(model="gpt-4", api_key= os.getenv("OPENAI_API_KEY"))

def solution_generator(prompt: str) -> CodeSolution:
    """
    Uses the LangChain agent to generate a CodeSolution based on the given prompt.
    """
    code_gen_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional programming assistant. Based on the user's requirements:
    1. Generate high-quality Python code.
    2. Include all necessary import statements.
    3. Write comprehensive unit tests to validate the solution.
    Ensure the code is executable and follows best practices."""),
        ("user", "{prompt}")
    ])
    code_gen = code_gen_prompt | llm.with_structured_output(CodeSolution)
    solution = code_gen.invoke({"prompt": prompt})
    return solution
