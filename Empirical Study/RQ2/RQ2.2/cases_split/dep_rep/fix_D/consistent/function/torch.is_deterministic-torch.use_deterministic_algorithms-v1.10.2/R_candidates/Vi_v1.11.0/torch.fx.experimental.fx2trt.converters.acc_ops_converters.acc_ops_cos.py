@tensorrt_converter(acc_ops.cos)
def acc_ops_cos(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.COS
    return add_unary_layer(network, input_val, operation_type, target, name)
