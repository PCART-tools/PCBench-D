def get_qconv_op(conv_op: Callable, has_relu: bool) -> Callable:
    qconv_op = {
        # has relu
        True: {
            torch.nn.functional.conv1d: torch.ops.quantized.conv1d_relu,
            torch.nn.functional.conv2d: torch.ops.quantized.conv2d_relu,
            torch.nn.functional.conv3d: torch.ops.quantized.conv3d_relu
        },
        False: {
            torch.nn.functional.conv1d: torch.ops.quantized.conv1d,
            torch.nn.functional.conv2d: torch.ops.quantized.conv2d,
            torch.nn.functional.conv3d: torch.ops.quantized.conv3d
        }
    }
    qconv = qconv_op[has_relu].get(conv_op)
    assert qconv, "Can't find corresponding quantized conv op for {} {}".format(conv_op, has_relu)
    return qconv
