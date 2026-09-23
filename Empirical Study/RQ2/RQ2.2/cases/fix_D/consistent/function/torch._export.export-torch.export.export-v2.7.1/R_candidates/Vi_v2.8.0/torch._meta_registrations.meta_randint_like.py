@register_meta([aten.randint_like.Tensor])
def meta_randint_like(self, high, **kwargs):
    return self.new_empty(self.size())
