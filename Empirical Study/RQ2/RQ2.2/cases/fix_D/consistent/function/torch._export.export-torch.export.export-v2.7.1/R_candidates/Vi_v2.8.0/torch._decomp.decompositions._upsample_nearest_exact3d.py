@register_decomposition(
    [aten._upsample_nearest_exact3d.default, aten._upsample_nearest_exact3d.out]
)
@aten._upsample_nearest_exact3d.default.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten._upsample_nearest_exact3d.default.py_impl(DispatchKey.Autograd)
@out_wrapper(preserve_memory_format=True, exact_dtype=True)
def _upsample_nearest_exact3d(
    input: Tensor,
    output_size: list[int],
    scales_d: Optional[float] = None,
    scales_h: Optional[float] = None,
    scales_w: Optional[float] = None,
) -> Tensor:
    return _upsample_nearest(
        input, output_size, [scales_d, scales_h, scales_w], exact=True
    )
