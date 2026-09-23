@register_acc_op_mapping(op_and_target=("call_function", torch.nn.functional.pad))
@register_acc_op
def pad(*, input, pad, mode, value):
    return torch.nn.functional.pad(input=input, pad=pad, mode=mode, value=value)
