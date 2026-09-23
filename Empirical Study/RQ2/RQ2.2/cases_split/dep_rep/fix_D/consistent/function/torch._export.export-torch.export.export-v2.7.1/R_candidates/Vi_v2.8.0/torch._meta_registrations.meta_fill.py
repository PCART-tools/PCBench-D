@register_meta([aten.fill.Tensor, aten.fill.Scalar])
def meta_fill(self, val):
    return torch.empty_like(self)
