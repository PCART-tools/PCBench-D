@tensorrt_converter(acc_ops.ceil)
def acc_ops_ceil(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.CEIL
    return add_unary_layer(network, input_val, operation_type, target, name)
