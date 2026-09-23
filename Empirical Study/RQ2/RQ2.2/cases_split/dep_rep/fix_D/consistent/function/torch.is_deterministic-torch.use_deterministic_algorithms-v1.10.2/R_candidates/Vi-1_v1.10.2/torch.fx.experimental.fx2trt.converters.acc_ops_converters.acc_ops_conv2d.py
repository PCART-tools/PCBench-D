@tensorrt_converter(acc_ops.conv2d)
def acc_ops_conv2d(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"Conv2d received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if has_dynamic_shape(input_val.shape):
        assert input_val.shape[1] != -1, "Channel dim can't be dynamic for convolution."

    # for now we'll assume bias is constant Tensor or None,
    # and bias being ITensor is not supported in TensorRT api
    # right now
    bias = to_numpy(kwargs["bias"])

    if network.has_explicit_precision:
        weight = get_trt_tensor(network, kwargs["weight"], f"{name}_weight")
        weight_shape = tuple(kwargs["weight"].shape)
        # will need to use uninitialized weight and set it later to support
        # ITensor weights
        dummy_weight = trt.Weights()

        layer = network.add_convolution(
            input=input_val,
            num_output_maps=weight.shape[0],
            kernel_shape=weight.shape[2:],
            kernel=dummy_weight,
            bias=bias,
        )

        layer.set_input(1, weight)
    else:
        weight = to_numpy(kwargs["weight"])
        layer = network.add_convolution(
            input=input_val,
            num_output_maps=weight.shape[0],
            kernel_shape=weight.shape[2:],
            kernel=weight,
            bias=bias,
        )

    layer.name = name
    layer.stride = kwargs["stride"]
    layer.padding = kwargs["padding"]
    layer.dilation = kwargs["dilation"]
    if kwargs["groups"] is not None:
        layer.num_groups = kwargs["groups"]

    return layer.get_output(0)
