def _prod_aten(
    inp: TensorLikeType,
    dims: Optional[DimsSequenceType],
    *,
    dtype: Optional[torch.dtype] = None,
) -> Tensor:
    if dims is not None:
        if len(dims) == 0:
            return inp.clone()
        for d in sorted(dims, reverse=True):
            assert d >= 0
            inp = torch.prod(inp, d, dtype=dtype)
        return inp
    else:
        return torch.prod(inp, dims, dtype=dtype)
