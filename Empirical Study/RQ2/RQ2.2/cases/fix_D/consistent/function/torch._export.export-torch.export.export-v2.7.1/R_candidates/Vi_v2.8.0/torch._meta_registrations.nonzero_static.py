@register_meta([aten.nonzero_static.default, aten.nonzero_static.out])
@out_wrapper()
def nonzero_static(self, *, size, fill_value: int = -1):
    return self.new_empty((size, self.dim()), dtype=torch.long)
