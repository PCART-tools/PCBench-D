@register_decomposition(aten.uniform)
@out_wrapper()
def uniform(
    x: Tensor,
    low: Union[bool, int, float] = 0.0,
    high: Union[bool, int, float] = 1.0,
    generator: Optional[torch.Generator] = None,
):
    return prims._uniform_helper(
        x.shape,
        low=sym_float(low),
        high=sym_float(high),
        dtype=x.dtype,
        device=x.device,
        generator=generator,
    )
