@tensorrt_converter(acc_ops.linear)
def acc_ops_linear(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"Linear received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    dynamic_dims = get_dynamic_dims(input_val.shape)
    assert len(dynamic_dims) < 2 and input_val.shape[-1] != -1, (
        "Currently we only support one dynmaic "
        "dim for linear and it can't be the last dim."
    )

    # TODO: Need to benchmark the performance of lowering linear as fully_connected versus
    # lowering as matmul + add. TensorRT documentation suggests to always lower it as
    # matmul + add but we found in some cases this results in performance regression compared
    # with lowering to fully_connected layer.
    layer = network.add_shuffle(input_val)
    layer.reshape_dims = tuple(input_val.shape) + (1, 1)
    set_layer_name(layer, target, f"{name}_pre_shuffle")
    bias = to_numpy(kwargs["bias"])  # type: ignore[arg-type]

    if network.has_explicit_precision:
        weight = get_trt_tensor(network, kwargs["weight"], f"{name}_weight")
        # will need to use uninitialized weight and set it later to support
        # ITensor weights
        dummy_weight = trt.Weights()

        # add fully connected
        layer = network.add_fully_connected(
            input=layer.get_output(0),
            num_outputs=weight.shape[0],
            kernel=dummy_weight,
            bias=bias,
        )
        layer.set_input(1, weight)
    else:
        weight = to_numpy(kwargs["weight"])  # type: ignore[arg-type]
        layer = network.add_fully_connected(
            input=layer.get_output(0),
            num_outputs=weight.shape[0],
            kernel=weight,
            bias=bias,
        )
    set_layer_name(layer, target, name)

    # reshape back
    layer = network.add_shuffle(layer.get_output(0))
    layer.reshape_dims = tuple(input_val.shape[:-1]) + (kwargs["weight"].shape[0],)  # type: ignore[union-attr]
    set_layer_name(layer, target, f"{name}_post_shuffle")

    return layer.get_output(0)
