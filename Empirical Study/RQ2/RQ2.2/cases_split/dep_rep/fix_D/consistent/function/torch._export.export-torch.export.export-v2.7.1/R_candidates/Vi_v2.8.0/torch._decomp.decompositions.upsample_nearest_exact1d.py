@register_decomposition(
    [aten._upsample_nearest_exact1d.default, aten._upsample_nearest_exact1d.out]
)
@aten._upsample_nearest_exact1d.default.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten._upsample_nearest_exact1d.default.py_impl(DispatchKey.Autograd)
@out_wrapper(preserve_memory_format=True, exact_dtype=True)
def upsample_nearest_exact1d(
    input: Tensor,
    output_size: list[int],
    scales: Optional[float] = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales], exact=True)
