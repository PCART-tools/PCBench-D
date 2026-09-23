@register_decomposition(aten.nansum)
@out_wrapper()
def nansum(self, dim=None, keepdim=False, *, dtype=None):
    return aten.sum(torch.where(torch.isnan(self), 0, self), dim, keepdim, dtype=dtype)
