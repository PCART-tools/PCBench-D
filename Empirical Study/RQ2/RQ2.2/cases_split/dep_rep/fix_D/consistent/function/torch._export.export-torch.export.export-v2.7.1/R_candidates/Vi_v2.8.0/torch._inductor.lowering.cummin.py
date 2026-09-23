@register_lowering(aten.cummin, type_promotion_kind=None)
def cummin(x, axis=None):
    if len(x.get_size()) == 0:
        assert axis in [0, -1]
        return clone(x), empty_like(x, dtype=torch.int64)

    dtype = x.get_dtype()
    combine_fn = ir.get_reduction_combine_fn(
        "argmin", dtype=dtype, arg_break_ties_left=False
    )

    kwargs = _make_scan_inner(x, axis=axis, dtype=dtype)
    kwargs["dtypes"] = (dtype, torch.int64)
    kwargs["inner_fns"] = (
        x.make_loader(),
        lambda idx: ops.index_expr(idx[axis], torch.int64),
    )
    values, indices = ir.Scan.create(**kwargs, combine_fn=combine_fn)  # type: ignore[arg-type]
    if values is None:
        return fallback_cummin(x, dim=axis)
    return values, indices
