def is_deterministic():
    r"""This function is deprecated and will be removed in a future release.
    Please use :func:`torch.are_deterministic_algorithms_enabled` instead.
    """
    warnings.warn((
        "torch.is_deterministic is deprecated and will be removed in a future "
        "release. Please use torch.are_deterministic_algorithms_enabled instead"))
    return are_deterministic_algorithms_enabled()
