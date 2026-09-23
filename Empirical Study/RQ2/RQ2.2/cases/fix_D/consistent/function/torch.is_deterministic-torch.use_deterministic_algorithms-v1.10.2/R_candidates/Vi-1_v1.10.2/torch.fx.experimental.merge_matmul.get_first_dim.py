def get_first_dim(t: torch.Tensor) -> int:
    """
    A free function primarily for use in the merge_matmul graph transformation below
    that returns the first dimension of a Tensor. This is necessary because torch.Tensor.shape
    is an attribute (and cannot be the target of a call_function node) and also helps save
    a getitem op in the graph.

    Arguments:
        t: The tensor to get the first dimension of.

    Returns:
        The first dimension of t.
    """
    return t.shape[0]
