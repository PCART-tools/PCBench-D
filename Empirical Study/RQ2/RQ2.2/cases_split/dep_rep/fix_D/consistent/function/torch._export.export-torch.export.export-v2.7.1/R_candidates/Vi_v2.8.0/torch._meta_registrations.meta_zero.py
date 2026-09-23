@register_meta(aten.zero.default)
def meta_zero(self):
    return self.new_empty(self.shape)
