@register_decomposition(aten.exponential)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("self",),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def exponential(self, rate=1, generator=None):
    assert generator is None
    torch._check(
        not utils.is_complex_dtype(self.dtype)
        and not utils.is_integer_dtype(self.dtype)
        and not utils.is_boolean_dtype(self.dtype),
        lambda: f"Exponential distribution is a continuous probability distribution. \
        dtype must be a floating point but you specified {self.dtype}",
    )
    torch._check(
        rate > 0.0,
        lambda: f"exponential_ expects lambda > 0.0, but found lambda={rate}",
    )

    uniform_val = torch.rand_like(self)

    # copying numerics of transformation::exponential see comment:
    # curand_uniform has (0,1] bounds. log(1) is 0 and exponential excludes 0.
    # we need log to be not 0, and not underflow when converted to half
    # fast __logf approximation can underflow, so set log to -epsilon/2 for 1 or close to 1 args
    epsilon = torch.finfo(uniform_val.dtype).eps / 2
    condition = uniform_val >= 1.0 - epsilon
    log_uniform = torch.where(condition, -epsilon, torch.log(uniform_val))

    return -1 / rate * log_uniform
