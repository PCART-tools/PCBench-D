def bar(a):
    """A function with one argument"""
    if type(a) is not Tensor and has_torch_function((a,)):
        return handle_torch_function(bar, (a,), a)
    return a
