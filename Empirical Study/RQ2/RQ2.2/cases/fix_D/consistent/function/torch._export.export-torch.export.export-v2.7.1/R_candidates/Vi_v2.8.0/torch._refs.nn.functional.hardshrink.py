@aten.hardshrink.default.py_impl(DispatchKey.Autograd)
@register_decomposition(aten.hardshrink)
@out_wrapper()
def hardshrink(a: TensorLikeType, lambd: float = 0.5):
    # Formula for reference,
    # hardshrink(x) = x if x > lambd
    #               = x if x < -lambd
    #               = 0 otherwise
    return torch.where(torch.abs(a) <= lambd, 0, a)
