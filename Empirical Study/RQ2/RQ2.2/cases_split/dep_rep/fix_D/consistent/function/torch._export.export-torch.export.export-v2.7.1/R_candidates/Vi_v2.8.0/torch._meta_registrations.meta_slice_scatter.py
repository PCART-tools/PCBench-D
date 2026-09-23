@register_meta(aten.slice_scatter.default)
def meta_slice_scatter(self, src, dim=0, start=None, end=None, step=1):
    return utils.clone_preserve_strides(self)
