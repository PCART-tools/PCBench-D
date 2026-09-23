@register_acc_op_mapping(op_and_target=("call_function", nn.functional.batch_norm))
@register_acc_op
def batch_norm(
    *, input, running_mean, running_var, weight, bias, training, momentum, eps
):
    return nn.functional.batch_norm(
        input=input,
        running_mean=running_mean,
        running_var=running_var,
        weight=weight,
        bias=bias,
        training=training,
        momentum=momentum,
        eps=eps,
    )
