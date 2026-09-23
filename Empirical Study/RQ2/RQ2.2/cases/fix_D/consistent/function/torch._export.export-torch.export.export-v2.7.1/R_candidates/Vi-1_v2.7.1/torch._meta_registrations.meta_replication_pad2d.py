@register_meta(aten.replication_pad2d)
@out_wrapper()
def meta_replication_pad2d(input, padding):
    return _pad2d_common(input, padding, is_reflection=False)
