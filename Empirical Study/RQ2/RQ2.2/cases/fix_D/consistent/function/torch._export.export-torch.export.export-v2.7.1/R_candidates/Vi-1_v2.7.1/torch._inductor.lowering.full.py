@register_lowering([torch.full, aten.full])
def full(size, fill_value, **kwargs):
    assert kwargs.get("dtype") is not None, "dtype should be handled by decomposition"
    return tensor_constructor(fill_value)(size, **kwargs)
