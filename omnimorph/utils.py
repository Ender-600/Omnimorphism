import inspect

def get_object_structure(obj):
    """
        class Person:
            def __init__(self, name, age):
                self.name = name    # str
                self.age = age      # int
                
        p = Person("Alice", 30)

    use get_object_structure(p) return:
        {'age': 'int', 'name': 'str'}
    """
    structure = {}
    for name, value in inspect.getmembers(obj):
        if name.startswith('__') or inspect.ismethod(value) or inspect.isfunction(value):
            continue
        structure[name] = type(value).__name__
    return structure

def get_class_name(obj):
    return type(obj).__name__

def get_module_of_object(obj):
    mod = inspect.getmodule(obj)
    return mod.__name__ if mod else None

def load_generated_code(code, obj):
    mod = inspect.getmodule(obj)
    global_env = globals().copy()
    if mod:
        global_env.update(vars(mod))
    local_env = {}
    exec(code, global_env, local_env)
    return local_env