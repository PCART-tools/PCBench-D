def tri(
    N,
    M=None,
    k=0,
    dtype: Optional[DTypeLike] = None,
    *,
    like: NotImplementedType = None,
):
    if M is None:
        M = N
    tensor = torch.ones((N, M), dtype=dtype)
    return torch.tril(tensor, diagonal=k)
