@register_decomposition(aten.norm)
@out_wrapper(exact_dtype=True)
def norm(
    input: TensorLikeType,
    p: Optional[Union[float, str]] = "fro",
    dim: Optional[DimsType] = None,
    keepdim: bool = False,
    *,
    dtype: Optional[torch.dtype] = None,
) -> TensorLikeType:
    # In these cases we compute the "Frobenius norm"
    if (
        p == "fro" and (dim is None or isinstance(dim, Dim) or len(dim) <= 2)
    ) or p is None:
        p = 2
    if isinstance(dim, Dim):
        dim = [dim]
    if isinstance(p, str):
        # Here we either call the nuclear norm, or we call matrix_norm with some arguments
        # that will throw an error
        if dim is None:
            dim = tuple(range(input.ndim))
        return torch.linalg.matrix_norm(input, p, dim, keepdim, dtype=dtype)
    else:
        return torch.linalg.vector_norm(input, p, dim, keepdim, dtype=dtype)
