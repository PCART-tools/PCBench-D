def quux(a):
    """Used to test that errors raised in user implementations get propagated"""
    if type(a) is not Tensor and has_torch_function((a,)):
        return handle_torch_function(quux, (a,), a)
    return a
