def _unsqueeze_atleast(
    at_least_fn: Callable, dim: int, arg: TensorLikeType
) -> TensorLikeType:
    arg_ = at_least_fn(arg)
    assert isinstance(arg_, TensorLike)
    return unsqueeze(arg_, dim)
