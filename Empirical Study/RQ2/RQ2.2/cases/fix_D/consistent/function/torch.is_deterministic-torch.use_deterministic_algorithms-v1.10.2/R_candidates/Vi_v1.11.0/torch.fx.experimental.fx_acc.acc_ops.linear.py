@register_acc_op_mapping(op_and_target=("call_function", nn.functional.linear))
@register_acc_op
def linear(*, input, weight, bias):
    return nn.functional.linear(input=input, weight=weight, bias=bias)
