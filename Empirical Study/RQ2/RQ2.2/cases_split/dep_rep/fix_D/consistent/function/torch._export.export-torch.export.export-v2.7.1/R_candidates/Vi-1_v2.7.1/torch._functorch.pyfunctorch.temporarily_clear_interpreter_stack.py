@contextlib.contextmanager
def temporarily_clear_interpreter_stack():
    stack = []
    try:
        while torch._C._functorch.peek_interpreter_stack() is not None:
            stack.append(pop_dynamic_layer_stack())
        yield list(stack)
    finally:
        while stack:
            push_dynamic_layer_stack(stack.pop())
