@register_acc_op_mapping(op_and_target=("call_function", nn.functional.layer_norm))
@register_acc_op
def layer_norm(*, input, normalized_shape, weight, bias, eps):
    return nn.functional.layer_norm(
        input=input,
        normalized_shape=normalized_shape,
        weight=weight,
        bias=bias,
        eps=eps,
    )
