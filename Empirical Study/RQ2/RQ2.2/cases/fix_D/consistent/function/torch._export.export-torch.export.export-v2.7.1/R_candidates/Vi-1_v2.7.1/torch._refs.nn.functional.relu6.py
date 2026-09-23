@register_decomposition(aten.relu6)
@_inplace_wrapper
@out_wrapper()
def relu6(a: TensorLikeType, inplace: bool = False) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.relu6
    """
    if inplace:
        raise NotImplementedError

    # See https://github.com/pytorch/pytorch/pull/81142#discussion_r918220126
    # It may be better to use clamp here, but we use hardtanh to replicate
    # the behavior of the existing implementation
    return torch.nn.functional.hardtanh(a, 0, 6)
