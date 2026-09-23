@register_meta(aten.reflection_pad1d)
@out_wrapper()
def meta_reflection_pad1d(input, padding):
    return _pad1d_common(input, padding, is_reflection=True)
