@aten.softshrink.default.py_impl(DispatchKey.Autograd)
@register_decomposition(aten.softshrink)
@out_wrapper()
def softshrink(a: TensorLikeType, lambd: float = 0.5):
    # Formula for reference,
    # softshrink(x) = x - lambd if x > lambd
    #               = x + lambd if x < -lambd
    #               = 0 otherwise
    torch._check(
        lambd >= 0,
        lambda: f"lambda must be greater or equal to 0, but found to be {lambd}",
    )
    # We implement this in one torch.where to generate better code in the backward
    # see https://github.com/pytorch/pytorch/pull/107052#discussion_r1293748211
    # We multiply by 0 for dealing with nans
    return torch.where(torch.abs(a) > lambd, a - torch.sign(a) * lambd, a * 0)
