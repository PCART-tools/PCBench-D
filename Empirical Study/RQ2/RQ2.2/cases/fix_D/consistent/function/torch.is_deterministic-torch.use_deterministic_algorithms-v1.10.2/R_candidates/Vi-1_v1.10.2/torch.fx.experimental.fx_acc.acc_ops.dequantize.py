@register_acc_op
def dequantize(*, input, input_tensor_meta):
    """`input_tensor_meta` contains extra argument of quantization
    parameters, e.g. scale/zero_point and will be using for
    lowring dequantize op to TensorRT
    """
    return torch.dequantize(input)
