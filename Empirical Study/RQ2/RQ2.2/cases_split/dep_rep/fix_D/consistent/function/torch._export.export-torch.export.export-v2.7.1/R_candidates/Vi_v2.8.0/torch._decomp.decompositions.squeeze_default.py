@register_decomposition([aten.squeeze.default, aten.squeeze.dim])
def squeeze_default(self: Tensor, dim: Optional[int] = None):
    # handle a scalar directly
    if not isinstance(self, torch.Tensor):
        return self
    # perform squeeze
    if dim is None:
        return aten.squeeze.dims(self, list(range(self.dim())))
    else:
        return aten.squeeze.dims(self, [dim])
