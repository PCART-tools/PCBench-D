@register_meta(aten.scatter_add_)
def meta_scatter_add_(self, dim, index, src):
    scatter_meta_impl(self, dim, index, src, "add")
    return self
