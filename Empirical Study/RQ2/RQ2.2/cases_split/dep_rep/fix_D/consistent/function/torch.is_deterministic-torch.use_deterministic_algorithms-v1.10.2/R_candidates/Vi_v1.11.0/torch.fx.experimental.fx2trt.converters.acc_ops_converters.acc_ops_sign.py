@tensorrt_converter(acc_ops.sign)
def acc_ops_sign(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if trt.__version__ >= "8.2" and not network.has_implicit_batch_dimension:
        input_val = kwargs["input"]
        operation_type = trt.UnaryOperation.SIGN
        return add_unary_layer(network, input_val, operation_type, target, name)

    return sign(network, input_val, target, name)
