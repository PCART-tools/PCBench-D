@register_meta(aten.select_scatter.default)
def meta_select_scatter(self, src, dim, index):
    return utils.clone_preserve_strides(self)
