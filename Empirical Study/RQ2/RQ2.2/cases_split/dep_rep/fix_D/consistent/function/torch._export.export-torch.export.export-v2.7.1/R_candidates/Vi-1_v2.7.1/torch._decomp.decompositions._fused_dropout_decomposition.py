@register_decomposition(aten._fused_dropout)
@out_wrapper("out0", "out1")
@pw_cast_for_opmath
def _fused_dropout_decomposition(input, p, generator=None):
    assert generator is None
    mask = (torch.rand_like(input) < p).to(dtype=torch.uint8)
    res = mask.type_as(input) * input * (1.0 / p)
    return (res, mask)
