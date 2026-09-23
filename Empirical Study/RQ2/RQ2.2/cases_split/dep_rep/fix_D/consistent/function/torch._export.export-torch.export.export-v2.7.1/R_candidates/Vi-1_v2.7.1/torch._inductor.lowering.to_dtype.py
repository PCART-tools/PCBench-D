def to_dtype(x: TensorBox, dtype: torch.dtype, copy=False):
    src_dtype = x.get_dtype()
    if src_dtype == dtype:
        return clone(x) if copy else x

    def _to_dtype(x):
        return ops.to_dtype(x, dtype, src_dtype=src_dtype)

    return make_pointwise(_to_dtype, override_return_dtype=dtype)(x)
