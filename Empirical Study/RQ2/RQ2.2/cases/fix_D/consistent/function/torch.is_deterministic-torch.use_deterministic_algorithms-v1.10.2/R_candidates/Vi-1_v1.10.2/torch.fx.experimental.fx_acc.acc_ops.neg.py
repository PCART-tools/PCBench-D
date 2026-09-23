@register_acc_op_mapping(op_and_target=("call_function", torch.neg))
@register_acc_op
def neg(*, input):
    return torch.neg(**locals())
