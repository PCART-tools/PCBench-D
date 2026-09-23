def pairwise_distance(x1: Tensor, x2: Tensor, p: float = 2.0, eps: float = 1e-6, keepdim: bool = False) -> Tensor:
    r"""
    See :class:`torch.nn.PairwiseDistance` for details
    """
    if has_torch_function_variadic(x1, x2):
        return handle_torch_function(pairwise_distance, (x1, x2), x1, x2, p=p, eps=eps, keepdim=keepdim)
    return torch.pairwise_distance(x1, x2, p, eps, keepdim)
