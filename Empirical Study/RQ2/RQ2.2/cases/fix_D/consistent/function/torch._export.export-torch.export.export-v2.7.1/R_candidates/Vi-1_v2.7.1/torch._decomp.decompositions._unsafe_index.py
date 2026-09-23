@register_decomposition([aten._unsafe_index])
def _unsafe_index(x, indices):
    return aten.index(x, indices)
