@parse_args("v", "v", "v", "is", "is", "is", "i", "is", "i", "i", "i", "i", "i")
def _convolution(g, input, weight, bias, stride, padding, dilation,
                 transposed, output_padding, groups, benchmark, deterministic, cudnn_enabled, allow_tf32):
    weight_size = sym_help._get_tensor_sizes(weight)
    try:
        kernel_shape = weight_size[2:]
    except Exception:
        kernel_shape = None

    if kernel_shape is None or any([i is None for i in kernel_shape]):
        raise RuntimeError("Unsupported: ONNX export of convolution for kernel "
                           "of unknown shape.")

    args = [input, weight]
    # ONNX only supports 1D bias
    if not sym_help._is_none(bias) and sym_help._get_tensor_rank(bias) == 1:
        args.append(bias)

    kwargs = {"kernel_shape_i": weight_size[2:],
              "strides_i": stride,
              # NB: ONNX supports asymmetric padding, whereas PyTorch supports only
              # symmetric padding
              "pads_i": padding + padding,
              "dilations_i": dilation,
              "group_i": groups}

    if any(o != 0 for o in output_padding):
        # ONNX supports both output_shape and output_padding. they are equivalent expressive.
        # output_padding is more straightforward, so we use it here.
        # output_shape = stride * (input_shape - 1) + output_padding + kernel_shape - padding * 2
        assert transposed
        assert len(stride) == len(output_padding)
        kwargs["output_padding_i"] = output_padding

    n = g.op("ConvTranspose" if transposed else "Conv", *args, **kwargs)

    if not sym_help._is_none(bias) and sym_help._get_tensor_rank(bias) != 1:
        return g.op("Add", n, bias)
    else:
        return n
