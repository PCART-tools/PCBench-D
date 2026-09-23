@tensorrt_converter(acc_ops.conv2d)
def acc_ops_conv2d(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"Conv2d received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if has_dynamic_shape(input_val.shape):
        assert input_val.shape[1] != -1, "Channel dim can't be dynamic for convolution."

    # for now we'll assume bias is constant Tensor or None,
    # and bias being ITensor is not supported in TensorRT api
    # right now
    if kwargs["bias"] is not None and not isinstance(kwargs["bias"], torch.Tensor):
        raise RuntimeError(
            f"linear {name} has bias of type {type(kwargs['bias'])}, Expect Optional[Tenosr]"
        )
    bias = to_numpy(kwargs["bias"])  # type: ignore[arg-type]

    if network.has_explicit_precision:
        weight = get_trt_tensor(network, kwargs["weight"], f"{name}_weight")
        weight_shape = tuple(kwargs["weight"].shape)  # type: ignore[union-attr]
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
        if not isinstance(kwargs["weight"], torch.Tensor):
            raise RuntimeError(
                f"linear {name} has weight of type {type(kwargs['weight'])}, Expect Optional[Tenosr]"
            )
        weight = to_numpy(kwargs["weight"])
        layer = network.add_convolution(
            input=input_val,
            num_output_maps=weight.shape[0],
            kernel_shape=weight.shape[2:],
            kernel=weight,
            bias=bias,
        )

    set_layer_name(layer, target, name)
    layer.stride = kwargs["stride"]
    layer.padding = kwargs["padding"]
    layer.dilation = kwargs["dilation"]
    if kwargs["groups"] is not None:
        layer.num_groups = kwargs["groups"]

    return layer.get_output(0)
