@register_meta([aten.poisson.default, aten.poisson.out])
@out_wrapper()
def meta_poisson(self, generator=None):
    return torch.empty_like(self)
