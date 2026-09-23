@register_decomposition([aten.upsample_nearest1d.default, aten.upsample_nearest1d.out])
@aten.upsample_nearest1d.default.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten.upsample_nearest1d.default.py_impl(DispatchKey.Autograd)
@out_wrapper(preserve_memory_format=True, exact_dtype=True)
def upsample_nearest1d(
    input: Tensor,
    output_size: list[int],
    scales: Optional[float] = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales])
