def has_tvm():
    try:
        importlib.import_module("tvm")
        return True
    except ImportError:
        return False
