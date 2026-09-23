@register_decomposition(aten.normal_)
def normal_(self, mean=0, std=1, *, generator=None):
    return normal(mean, std, self.shape, out=self, generator=generator)
