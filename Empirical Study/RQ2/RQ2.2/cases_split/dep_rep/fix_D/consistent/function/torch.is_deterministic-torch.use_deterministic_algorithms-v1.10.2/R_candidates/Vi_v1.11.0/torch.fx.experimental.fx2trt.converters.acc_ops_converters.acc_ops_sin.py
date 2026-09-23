@tensorrt_converter(acc_ops.sin)
def acc_ops_sin(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.SIN
    return add_unary_layer(network, input_val, operation_type, target, name)
