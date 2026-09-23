@register_meta(aten.scalar_tensor.default)
def scalar_tensor(s, dtype=None, layout=None, device=None, pin_memory=None):
    # NB: It's always wrong to try to create a scalar tensor with the jagged layout.
    # Rather than fix this everywhere, just use the strided layout and let NJT handle
    # scalar tensor broadcasting.
    if layout == torch.jagged:
        layout = torch.strided
    return torch.empty(
        (), dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )
