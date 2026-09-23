@register_meta(aten.silu)
@out_wrapper(exact_dtype=True)
def silu(self: Tensor) -> Tensor:
    return torch.empty_like(self)
