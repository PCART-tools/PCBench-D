@register_op_impl(torch.ops.aten.nonzero_numpy.default)
def nonzero_numpy(fake_mode, func, arg):
    return torch.ops.aten.nonzero.default(arg).unbind(1)
