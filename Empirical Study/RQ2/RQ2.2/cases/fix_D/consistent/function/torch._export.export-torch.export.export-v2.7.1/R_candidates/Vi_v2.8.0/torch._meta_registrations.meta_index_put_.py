@register_meta(aten.index_put_.default)
def meta_index_put_(self, indices, values, accumulate=False):
    return self
