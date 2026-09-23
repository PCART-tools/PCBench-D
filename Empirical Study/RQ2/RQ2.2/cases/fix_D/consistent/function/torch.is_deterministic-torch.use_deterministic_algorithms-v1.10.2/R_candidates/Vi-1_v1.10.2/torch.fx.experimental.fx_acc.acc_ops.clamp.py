@register_acc_op_mapping(op_and_target=("call_function", torch.clamp))
@register_acc_op_mapping(op_and_target=("call_method", "clamp"))
@register_acc_op
def clamp(*, input, min, max):
    return torch.clamp(**locals())
