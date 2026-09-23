@register_decomposition(aten.upsample_nearest1d.vec)
@register_decomposition(aten.upsample_nearest2d.vec)
@register_decomposition(aten.upsample_nearest3d.vec)
@aten.upsample_nearest1d.vec.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten.upsample_nearest1d.vec.py_impl(DispatchKey.Autograd)
@aten.upsample_nearest2d.vec.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten.upsample_nearest2d.vec.py_impl(DispatchKey.Autograd)
@aten.upsample_nearest3d.vec.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten.upsample_nearest3d.vec.py_impl(DispatchKey.Autograd)
def _upsample_nearest_vec(
    input: Tensor,
    output_size: Optional[list[int]],
    scale_factors: Optional[list[float]],
) -> Tensor:
    osize = upsample_compute_output_size(input.size(), output_size, scale_factors)
    scales = (
        scale_factors if scale_factors else [None] * len(osize)  # type: ignore[list-item]
    )
    return _upsample_nearest(input, osize, scales)
