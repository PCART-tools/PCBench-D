@register_acc_op_mapping(op_and_target=("call_function", torch.sigmoid))
@register_acc_op_mapping(op_and_target=("call_method", "sigmoid"))
@register_acc_op
def sigmoid(*, input):
    return torch.sigmoid(**locals())
