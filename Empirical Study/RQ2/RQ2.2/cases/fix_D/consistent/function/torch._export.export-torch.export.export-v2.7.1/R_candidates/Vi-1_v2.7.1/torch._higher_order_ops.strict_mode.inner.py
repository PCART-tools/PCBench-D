@strict_mode_op.py_impl(ProxyTorchDispatchMode)
def inner(mode, callable, operands):
    return trace_strict_mode(mode, strict_mode_op, callable, operands)
