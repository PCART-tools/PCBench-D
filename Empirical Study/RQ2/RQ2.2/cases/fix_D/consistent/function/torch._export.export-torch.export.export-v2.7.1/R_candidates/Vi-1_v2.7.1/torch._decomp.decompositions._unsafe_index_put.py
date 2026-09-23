@register_decomposition([aten._unsafe_index_put])
def _unsafe_index_put(x, indices, value, accumulate=False):
    return aten.index_put(x, indices, value, accumulate)
