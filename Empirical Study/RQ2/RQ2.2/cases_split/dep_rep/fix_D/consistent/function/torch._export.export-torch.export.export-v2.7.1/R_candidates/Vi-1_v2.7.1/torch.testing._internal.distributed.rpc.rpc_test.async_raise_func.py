@rpc.functions.async_execution
def async_raise_func():
    raise RuntimeError("Expected error")
