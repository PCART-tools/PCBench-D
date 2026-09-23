@register_extra_random_decomp([aten.bernoulli.p])
def bernoulli_p(self, p=0.5, *, generator=None):
    if self.device == torch.device("cpu"):
        return NotImplemented
    assert generator is None
    return torch.rand_like(self, dtype=torch.float32) < p
