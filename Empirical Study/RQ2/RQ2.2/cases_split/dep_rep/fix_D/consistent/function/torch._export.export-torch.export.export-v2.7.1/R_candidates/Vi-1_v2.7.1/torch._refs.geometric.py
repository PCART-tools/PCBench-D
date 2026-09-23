@register_decomposition(aten.geometric)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("self",),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def geometric(self, p, generator=None):
    assert generator is None
    # TODO: fix inductor rand_like for integer, bool dtypes
    torch._check(
        not utils.is_complex_dtype(self.dtype)
        and not utils.is_boolean_dtype(self.dtype),
        lambda: f"geometric not implemented for {self.dtype}",
    )
    torch._check(
        0 < p and p < 1,
        lambda: f"geometric_ expects p to be in (0, 1), but got p={p}",
    )
    return torch.floor(torch.log1p(-torch.rand_like(self)) / math.log1p(-p)) + 1
