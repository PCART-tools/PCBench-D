@register_decomposition(aten.count_nonzero)
@out_wrapper()
def count_nonzero(self, dim: Optional[DimsType] = None):
    return (self != 0).sum(dim)
