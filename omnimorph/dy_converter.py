import os
import hashlib
import inspect
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import initialize_agent, Tool, AgentType

load_dotenv()
llm = ChatOpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'generated')
os.makedirs(CACHE_DIR, exist_ok=True)

from .conversion_registry import register_conversion, get_conversion
from omnimorph.utils import get_object_structure, get_class_name, load_generated_code, sanitize_code

def conversion_tool(query: str) -> str:
    prompt_template = ChatPromptTemplate.from_template(query)
    chain = prompt_template | llm | StrOutputParser()
    code = chain.invoke({})
    return code

conversion_code_tool = Tool(
    name="ConversionCodeGenerator",
    func=conversion_tool,
    description="Generates Python conversion code from a source object type to a target library. "
                "The query should include the source type name, its attributes, and target library information."
)

agent = initialize_agent(
    tools=[conversion_code_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

class DynamicConverter:
    def __init__(self, obj):
        self.obj = obj
        self.class_name = get_class_name(obj)

    def generate_conversion_code(self, target_lib: str) -> str:
        struct = self.get_object_structure(self.obj)
        struct_str = str(struct).replace("{", "{{").replace("}", "}}")
        prompt = f"""
You are an expert Python developer.
Generate a Python function that converts an object of type {self.class_name} into an object compatible with target library "{target_lib}".
The source object has the following attributes and their types: {struct_str}.
The generated function must be named "convert_{self.class_name}_to_{target_lib.lower()}" and take a single argument 'obj'.
Return only the Python function code without any additional explanation.
"""
        prompt_obj = ChatPromptTemplate.from_template(prompt)
        input_variables = {
            "source_type": self.class_name,
            "target_library": target_lib,
            "attributes": struct_str,
            "function_name": f"convert_{self.class_name}_to_{target_lib.lower()}",
            "argument_name": "obj"
        }
        chain = prompt_obj | llm | StrOutputParser()
        code = chain.invoke(input_variables)
        return code

    def save_conversion_code(self, target_lib: str, code: str) -> str:
        hash_key = hashlib.md5((self.class_name + target_lib).encode()).hexdigest()
        filename = f"{self.class_name}_to_{target_lib.lower()}_{hash_key}.py"
        filepath = os.path.join(CACHE_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        return filepath

    def load_and_register_conversion(self, target_lib: str):
        conv_func = get_conversion(type(self.obj), target_lib)
        if conv_func is not None:
            return conv_func

        code = self.generate_conversion_code(target_lib)
        code = sanitize_code(code)                                  # Remove unnecessary lines
        filepath = self.save_conversion_code(target_lib, code)
        namespace = load_generated_code(code, self.obj)
        func_name = f"convert_{self.class_name}_to_{target_lib.lower()}"
        if func_name not in namespace:
            raise ValueError(f"Generated function {func_name} not found in code from {filepath}.")
        conv_func = namespace[func_name]
        register_conversion(type(self.obj), target_lib, conv_func)
        return conv_func

    def to(self, target_lib: str, *args, **kwargs):
        
        conv_func = self.load_and_register_conversion(target_lib)
        return conv_func(self.obj, *args, **kwargs)