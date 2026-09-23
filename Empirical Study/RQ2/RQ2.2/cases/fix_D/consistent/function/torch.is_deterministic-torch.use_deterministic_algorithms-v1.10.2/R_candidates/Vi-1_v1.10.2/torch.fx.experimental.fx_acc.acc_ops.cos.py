@register_acc_op_mapping(op_and_target=("call_function", torch.cos))
@register_acc_op
def cos(*, input):
    return torch.cos(**locals())
