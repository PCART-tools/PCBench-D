@register_decomposition([aten.upsample_nearest3d.default, aten.upsample_nearest3d.out])
@aten.upsample_nearest3d.default.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten.upsample_nearest3d.default.py_impl(DispatchKey.Autograd)
@out_wrapper(preserve_memory_format=True, exact_dtype=True)
def upsample_nearest3d(
    input: Tensor,
    output_size: list[int],
    scales_d: Optional[float] = None,
    scales_h: Optional[float] = None,
    scales_w: Optional[float] = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales_d, scales_h, scales_w])
