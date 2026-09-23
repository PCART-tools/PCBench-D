def _load_obj_from_str(fully_qualified_name):
    module, obj_name = fully_qualified_name.rsplit(".", maxsplit=1)
    return getattr(importlib.import_module(module), obj_name)
