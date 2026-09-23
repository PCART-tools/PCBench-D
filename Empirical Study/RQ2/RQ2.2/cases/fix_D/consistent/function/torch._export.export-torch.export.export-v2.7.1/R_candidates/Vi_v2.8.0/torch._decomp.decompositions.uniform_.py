@register_decomposition(aten.uniform_)
def uniform_(self, low=0, high=1, generator=None):
    return self.copy_(uniform(self, low, high, generator))
