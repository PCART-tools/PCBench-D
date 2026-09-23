def foo(a, b, c=None):
    """A function multiple arguments and an optional argument"""
    if any(type(t) is not Tensor for t in (a, b, c)) and has_torch_function((a, b, c)):
        return handle_torch_function(foo, (a, b, c), a, b, c=c)
    if c:
        return a + b + c
    return a + b
