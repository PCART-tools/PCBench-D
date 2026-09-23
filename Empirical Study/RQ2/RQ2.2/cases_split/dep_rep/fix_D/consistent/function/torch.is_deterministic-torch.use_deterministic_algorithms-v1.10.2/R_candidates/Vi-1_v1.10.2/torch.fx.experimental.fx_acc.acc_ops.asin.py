@register_acc_op_mapping(op_and_target=("call_function", torch.asin))
@register_acc_op
def asin(*, input):
    return torch.asin(**locals())
