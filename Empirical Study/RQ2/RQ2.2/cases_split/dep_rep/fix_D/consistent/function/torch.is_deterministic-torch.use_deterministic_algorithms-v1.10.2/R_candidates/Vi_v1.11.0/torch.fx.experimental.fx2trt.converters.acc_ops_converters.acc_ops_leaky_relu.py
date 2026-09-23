@tensorrt_converter(acc_ops.leaky_relu)
def acc_ops_leaky_relu(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    negative_slope = kwargs["negative_slope"]
    operation_type = trt.ActivationType.LEAKY_RELU
    return add_activation_layer(network, input_val, operation_type, target, name, negative_slope)
