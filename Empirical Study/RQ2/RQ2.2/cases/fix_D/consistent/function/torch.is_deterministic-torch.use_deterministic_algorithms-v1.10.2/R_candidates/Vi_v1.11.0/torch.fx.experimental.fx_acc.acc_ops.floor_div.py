@register_acc_op_properties(AccOpProperty.pointwise)
@register_acc_op_mapping(op_and_target=("call_function", operator.floordiv))
@register_acc_op
def floor_div(*, input, other):
    # This is temp fix because currently operator.floor_div for tensors would
    # traslate into torch.floor_divide which would throw an error. After it's
    # fixed we can stick to `input // other`.
    if isinstance(input, torch.Tensor) or isinstance(other, torch.Tensor):
        return torch.div(input, other, rounding_mode="floor")
    return input // other
