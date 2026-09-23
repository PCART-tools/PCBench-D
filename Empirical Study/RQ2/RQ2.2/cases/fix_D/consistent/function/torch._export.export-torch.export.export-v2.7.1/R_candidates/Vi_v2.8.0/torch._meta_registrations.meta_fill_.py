@register_meta([aten.fill_.Tensor, aten.fill_.Scalar])
def meta_fill_(self, val):
    return self
