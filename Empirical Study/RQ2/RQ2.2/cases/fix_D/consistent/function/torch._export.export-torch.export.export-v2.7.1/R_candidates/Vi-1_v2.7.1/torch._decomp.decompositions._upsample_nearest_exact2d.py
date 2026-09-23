@register_decomposition(
    [aten._upsample_nearest_exact2d.default, aten._upsample_nearest_exact2d.out]
)
@aten._upsample_nearest_exact2d.default.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten._upsample_nearest_exact2d.default.py_impl(DispatchKey.Autograd)
@out_wrapper(preserve_memory_format=True, exact_dtype=True)
def _upsample_nearest_exact2d(
    input: Tensor,
    output_size: list[int],
    scales_h: Optional[float] = None,
    scales_w: Optional[float] = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales_h, scales_w], exact=True)
