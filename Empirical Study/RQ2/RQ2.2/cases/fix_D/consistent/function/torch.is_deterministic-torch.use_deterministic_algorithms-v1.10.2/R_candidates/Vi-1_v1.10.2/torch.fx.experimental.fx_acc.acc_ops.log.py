@register_acc_op_mapping(op_and_target=("call_function", torch.log))
@register_acc_op
def log(*, input):
    return torch.log(**locals())
