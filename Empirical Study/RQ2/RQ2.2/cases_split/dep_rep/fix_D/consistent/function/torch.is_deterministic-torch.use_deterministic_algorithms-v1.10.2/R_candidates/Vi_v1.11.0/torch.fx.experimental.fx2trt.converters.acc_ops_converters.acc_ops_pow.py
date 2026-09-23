@tensorrt_converter(acc_ops.pow)
def acc_ops_pow(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["exponent"], trt.ElementWiseOperation.POW, target, name
    )
