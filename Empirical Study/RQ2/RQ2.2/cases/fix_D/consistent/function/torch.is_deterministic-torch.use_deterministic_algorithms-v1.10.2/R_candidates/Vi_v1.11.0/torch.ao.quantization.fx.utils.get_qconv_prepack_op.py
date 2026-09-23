def get_qconv_prepack_op(conv_op: Callable) -> Callable:
    prepack_ops = {
        torch.nn.functional.conv1d: torch.ops.quantized.conv1d_prepack,
        torch.nn.functional.conv2d: torch.ops.quantized.conv2d_prepack,
        torch.nn.functional.conv3d: torch.ops.quantized.conv3d_prepack
    }
    prepack_op = prepack_ops.get(conv_op, None)
    assert prepack_op, "Didn't find prepack op for {}".format(conv_op)
    return prepack_op
