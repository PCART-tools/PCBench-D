@register_acc_op_mapping(op_and_target=("call_function", torch.sqrt))
@register_acc_op
def sqrt(*, input):
    return torch.sqrt(**locals())
