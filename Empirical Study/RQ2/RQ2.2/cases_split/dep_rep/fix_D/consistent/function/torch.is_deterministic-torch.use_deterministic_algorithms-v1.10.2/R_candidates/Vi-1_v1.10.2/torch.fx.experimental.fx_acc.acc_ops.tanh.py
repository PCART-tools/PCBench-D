@register_acc_op_mapping(op_and_target=("call_function", torch.tanh))
@register_acc_op
def tanh(*, input):
    return torch.tanh(**locals())
