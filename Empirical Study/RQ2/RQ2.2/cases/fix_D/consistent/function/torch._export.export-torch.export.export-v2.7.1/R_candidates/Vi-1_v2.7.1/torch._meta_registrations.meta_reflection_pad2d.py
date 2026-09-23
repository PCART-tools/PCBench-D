@register_meta(aten.reflection_pad2d)
@out_wrapper()
def meta_reflection_pad2d(input, padding):
    return _pad2d_common(input, padding, is_reflection=True)
