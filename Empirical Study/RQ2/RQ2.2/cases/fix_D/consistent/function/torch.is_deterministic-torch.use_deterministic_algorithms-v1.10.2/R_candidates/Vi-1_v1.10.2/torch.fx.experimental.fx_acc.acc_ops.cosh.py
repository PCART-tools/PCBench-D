@register_acc_op_mapping(op_and_target=("call_function", torch.cosh))
@register_acc_op
def cosh(*, input):
    return torch.cosh(**locals())
