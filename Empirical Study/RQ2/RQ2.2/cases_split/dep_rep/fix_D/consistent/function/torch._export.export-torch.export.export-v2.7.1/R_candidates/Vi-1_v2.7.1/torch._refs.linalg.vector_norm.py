@register_decomposition(torch._ops.ops.aten.linalg_vector_norm)
@out_wrapper(exact_dtype=True)
def vector_norm(
    x: TensorLikeType,
    ord: Union[float, int] = 2,
    dim: Optional[DimsType] = None,
    keepdim: bool = False,
    *,
    dtype: Optional[torch.dtype] = None,
) -> Tensor:
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    # Checks
    check_fp_or_complex(x.dtype, "linalg.vector_norm")

    if isinstance(dim, Dim):
        dim = [dim]  # type: ignore[assignment]

    if guard_size_oblivious(x.numel() == 0) and (ord < 0.0 or ord == float("inf")):
        torch._check(
            dim is not None and len(dim) != 0,
            lambda: f"linalg.vector_norm cannot compute the {ord} norm on an empty tensor "
            "because the operation does not have an identity",
        )
        shape = x.shape
        assert dim is not None  # mypy does not seem to be able to see through check?
        for d in dim:
            torch._check(
                shape[d] != 0,
                lambda: f"linalg.vector_norm cannot compute the {ord} norm on the "
                f"dimension {d} because this dimension is empty and the "
                "operation does not have an identity",
            )
    _check_norm_dtype(dtype, x.dtype, "linalg.vector_norm")

    computation_dtype, result_dtype = utils.reduction_dtypes(
        x, utils.REDUCTION_OUTPUT_TYPE_KIND.COMPLEX_TO_FLOAT, dtype
    )

    to_result_dtype = partial(_maybe_convert_to_dtype, dtype=result_dtype)

    # Implementation
    if ord == 0.0:
        return torch.sum(torch.ne(x, 0.0), dim=dim, keepdim=keepdim, dtype=result_dtype)
    elif ord == float("inf"):
        return to_result_dtype(torch.amax(torch.abs(x), dim=dim, keepdim=keepdim))  # type: ignore[return-value,arg-type]
    elif ord == float("-inf"):
        return to_result_dtype(torch.amin(torch.abs(x), dim=dim, keepdim=keepdim))  # type: ignore[return-value,arg-type]
    else:
        # From here on the computation dtype is important as the reduction is non-trivial
        x = _maybe_convert_to_dtype(x, computation_dtype)  # type: ignore[assignment]
        reduce_sum = partial(torch.sum, dim=dim, keepdim=keepdim)

        is_ord_even = ord % 2 == 0 if isinstance(ord, IntLike) else ord % 2.0 == 0.0
        if not (is_ord_even and utils.is_float_dtype(x.dtype)):
            x = torch.abs(x)
        return to_result_dtype(torch.pow(reduce_sum(torch.pow(x, ord)), 1.0 / ord))  # type: ignore[return-value]
