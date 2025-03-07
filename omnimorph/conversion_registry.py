conversion_registry = {}

def register_conversion(source_class, target_lib, func):
    key = (source_class.__name__, target_lib.lower())
    conversion_registry[key] = func

def get_conversion(source_class, target_lib):
    key = (source_class.__name__, target_lib.lower())
    return conversion_registry.get(key)

def all_conversions():
    return conversion_registry