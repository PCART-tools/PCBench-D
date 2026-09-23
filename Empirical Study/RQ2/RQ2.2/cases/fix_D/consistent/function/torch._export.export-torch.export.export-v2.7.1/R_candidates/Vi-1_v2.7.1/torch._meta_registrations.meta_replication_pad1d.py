@register_meta(aten.replication_pad1d)
@out_wrapper()
def meta_replication_pad1d(input, padding):
    return _pad1d_common(input, padding, is_reflection=False)
