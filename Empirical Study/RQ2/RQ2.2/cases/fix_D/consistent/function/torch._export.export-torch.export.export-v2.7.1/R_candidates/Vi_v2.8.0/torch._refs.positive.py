def positive(a: TensorLikeType) -> TensorLikeType:
    assert isinstance(a, TensorLike)
    if a.dtype is torch.bool:
        msg = "positive does not support bool tensors."
        raise RuntimeError(msg)
    return a
