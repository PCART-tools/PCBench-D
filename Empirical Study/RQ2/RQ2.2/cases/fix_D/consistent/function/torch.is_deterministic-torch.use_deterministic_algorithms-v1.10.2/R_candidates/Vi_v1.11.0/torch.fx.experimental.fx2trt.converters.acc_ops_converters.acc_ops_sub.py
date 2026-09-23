@tensorrt_converter(acc_ops.sub)
def acc_ops_sub(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["other"], trt.ElementWiseOperation.SUB, target, name
    )
