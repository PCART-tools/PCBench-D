def _pop_mode():
    old = _pop_torch_function_stack()
    return old
