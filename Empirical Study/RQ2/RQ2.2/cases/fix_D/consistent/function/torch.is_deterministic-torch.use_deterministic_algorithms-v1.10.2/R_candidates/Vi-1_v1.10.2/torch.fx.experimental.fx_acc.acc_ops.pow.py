@register_acc_op_mapping(op_and_target=("call_function", torch.pow))
@register_acc_op
def pow(*, input, exponent):
    return torch.pow(input, exponent)
