@tensorrt_converter(acc_ops.cosh)
def acc_ops_cosh(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.COSH
    return add_unary_layer(network, input_val, operation_type, target, name)
