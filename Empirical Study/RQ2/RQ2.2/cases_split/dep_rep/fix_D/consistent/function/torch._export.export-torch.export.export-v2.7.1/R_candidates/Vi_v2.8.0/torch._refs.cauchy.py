@register_decomposition(aten.cauchy)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("self",),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def cauchy(self, median=0, sigma=1, generator=None):
    assert generator is None
    torch._check(
        not utils.is_complex_dtype(self.dtype)
        and not utils.is_integer_dtype(self.dtype)
        and not utils.is_boolean_dtype(self.dtype),
        lambda: f"Cauchy distribution is a continuous probability distribution. \
        dtype must be a floating point but you specified {self.dtype}",
    )
    torch._check(
        sigma > 0.0,
        lambda: f"cauchy_ expects sigma > 0.0, but found sigma={sigma}",
    )
    return median + sigma * torch.tan(math.pi * (torch.rand_like(self) - 0.5))
