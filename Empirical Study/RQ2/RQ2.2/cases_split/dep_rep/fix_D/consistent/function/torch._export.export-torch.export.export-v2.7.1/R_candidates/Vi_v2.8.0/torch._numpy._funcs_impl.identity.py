def identity(n, dtype: Optional[DTypeLike] = None, *, like: NotImplementedType = None):
    return torch.eye(n, dtype=dtype)
