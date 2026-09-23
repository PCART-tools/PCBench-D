@register_meta([aten.complex.default, aten.complex.out])
@out_wrapper()
def meta_complex(real, imag):
    assert real.dtype.is_floating_point
    assert imag.dtype.is_floating_point
    out_shape = _broadcast_shapes(real.shape, imag.shape)
    return real.new_empty(out_shape, dtype=corresponding_complex_dtype(real.dtype))
