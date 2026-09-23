@register_acc_op_mapping(op_and_target=("call_function", nn.functional.batch_norm))
@register_acc_op
def batch_norm(
    *, input, running_mean, running_var, weight, bias, training, momentum, eps
):
    return nn.functional.batch_norm(**locals())
