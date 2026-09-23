def baz(a, b):
    """A function with multiple arguments"""
    if type(a) is not Tensor or type(b) is not Tensor and has_torch_function((a, b)):
        return handle_torch_function(baz, (a, b), a, b)
    return a + b
