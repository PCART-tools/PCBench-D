def _supported_head_dim(n: Union[int, torch.SymInt]) -> bool:
    """Returns true if the head dim is supported by FlexAttention"""
    return n in _SUPPORTED_HEAD_DIMS
