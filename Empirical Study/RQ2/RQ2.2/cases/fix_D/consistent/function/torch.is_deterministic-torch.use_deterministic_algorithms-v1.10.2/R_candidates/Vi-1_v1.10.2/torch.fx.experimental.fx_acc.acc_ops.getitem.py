@register_acc_op_mapping(op_and_target=("call_function", operator.getitem))
@register_acc_op
def getitem(*, input, idx):
    return input[idx]
