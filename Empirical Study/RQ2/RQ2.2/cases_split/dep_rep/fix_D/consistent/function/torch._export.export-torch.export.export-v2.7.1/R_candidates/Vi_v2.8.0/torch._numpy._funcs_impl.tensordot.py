def tensordot(a: ArrayLike, b: ArrayLike, axes=2):
    if isinstance(axes, (list, tuple)):
        axes = [[ax] if isinstance(ax, int) else ax for ax in axes]

    target_dtype = _dtypes_impl.result_type_impl(a, b)
    a = _util.cast_if_needed(a, target_dtype)
    b = _util.cast_if_needed(b, target_dtype)

    return torch.tensordot(a, b, dims=axes)
