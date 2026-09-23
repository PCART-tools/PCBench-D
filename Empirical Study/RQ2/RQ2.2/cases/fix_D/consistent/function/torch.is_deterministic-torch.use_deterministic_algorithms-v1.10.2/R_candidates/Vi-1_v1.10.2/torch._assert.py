def _assert(condition, message):
    r"""A wrapper around Python's assert which is symbolically traceable.
    """
    from .overrides import has_torch_function, handle_torch_function

    if type(condition) is not torch.Tensor and has_torch_function((condition,)):
        return handle_torch_function(_assert, (condition,), condition, message)
    assert condition, message
