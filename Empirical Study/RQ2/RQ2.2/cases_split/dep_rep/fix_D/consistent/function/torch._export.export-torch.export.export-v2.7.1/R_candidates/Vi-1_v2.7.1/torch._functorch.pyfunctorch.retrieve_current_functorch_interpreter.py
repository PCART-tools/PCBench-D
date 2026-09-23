def retrieve_current_functorch_interpreter() -> FuncTorchInterpreter:
    interpreter = torch._C._functorch.peek_interpreter_stack()
    assert interpreter is not None
    return coerce_cinterpreter(interpreter)
