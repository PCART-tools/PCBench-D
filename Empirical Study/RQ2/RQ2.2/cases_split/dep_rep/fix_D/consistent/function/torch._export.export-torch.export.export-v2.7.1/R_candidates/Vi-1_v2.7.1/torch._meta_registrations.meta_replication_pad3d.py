@register_meta(aten.replication_pad3d)
@out_wrapper()
def meta_replication_pad3d(input, padding):
    return _pad3d_common(input, padding, is_reflection=False)
