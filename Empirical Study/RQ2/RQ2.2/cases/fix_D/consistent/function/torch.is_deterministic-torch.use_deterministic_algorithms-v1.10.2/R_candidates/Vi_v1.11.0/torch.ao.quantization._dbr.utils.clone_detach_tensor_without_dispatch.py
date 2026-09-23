def clone_detach_tensor_without_dispatch(x: torch.Tensor) -> torch.Tensor:
    """
    Creates a detached clone of `x`, unwrapping x from any dispatched
    type before performing the copy.
    This is necessary to not leak dispatched types to debugging logic
    such as numeric suite.
    TODO(future PR): figure out why is_quantized returns False for
    the dispatched types, even though the underlying tensor is quantized.
    """
    old_class = x.__class__
    x.__class__ = torch.Tensor
    x_copy = x.clone().detach()
    x.__class__ = old_class
    return x_copy
