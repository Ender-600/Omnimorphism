from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os
import re
import hashlib
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))

CACHE_DIR = "./generated/"
os.makedirs(CACHE_DIR, exist_ok=True)

class Omnimorph:
    def __init__(self, obj):
        self.obj = obj
        self.class_name = type(obj).__name__

    def __getattr__(self, method_name):
        def wrapper(*args, **kwargs):
            cache_file = self._get_cache_file(method_name)
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    code = f.read()
            else:
                code = self._generate_code(method_name)
                with open(cache_file, 'w') as f:
                    f.write(code)

            local_vars = {}
            exec(code, globals(), local_vars)
            return local_vars[method_name](self.obj, *args, **kwargs)

        return wrapper

    def _get_cache_file(self, method_name):
        key = hashlib.md5((self.class_name + method_name).encode()).hexdigest()
        return os.path.join(CACHE_DIR, f"{self.class_name}_{method_name}_{key}.py")

    def _generate_code(self, method_name):
        attrs = dir(self.obj)
        prompt_template = ChatPromptTemplate.from_template(
            """
            You are generating Python code. STRICTLY return ONLY Python code.
            Do NOT include ANY text other than the pure Python function.

            Generate exactly this function:

            def {method_name}(item, *args, **kwargs):
                # Implement logic based on class '{class_name}' with attributes/methods: {attrs}.
                pass
            """
        )
        print("line 55")
        chain = prompt_template | llm | StrOutputParser()
        code = chain.invoke({
            "class_name": self.class_name,
            "attrs": attrs,
            "method_name": method_name
        })
    
        return code

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    class Box:
        def __init__(self, mass):
            self.mass = mass

    box = Box(12.5)
    om_box = Omnimorph(box)

    print("Is heavy:", om_box.is_heavy(threshold=10.0))
