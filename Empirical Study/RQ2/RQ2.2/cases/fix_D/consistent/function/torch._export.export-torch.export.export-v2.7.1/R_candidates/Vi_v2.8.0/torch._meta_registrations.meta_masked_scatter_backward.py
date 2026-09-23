@register_meta(aten.masked_scatter_backward)
def meta_masked_scatter_backward(self, mask, sizes):
    return self.new_empty(sizes)
