@register_decomposition(aten.aminmax)
@out_wrapper("min", "max")
def aminmax(self, *, dim=None, keepdim=False):
    amin = torch.amin(self, dim=dim, keepdim=keepdim)
    amax = torch.amax(self, dim=dim, keepdim=keepdim)
    return amin, amax
