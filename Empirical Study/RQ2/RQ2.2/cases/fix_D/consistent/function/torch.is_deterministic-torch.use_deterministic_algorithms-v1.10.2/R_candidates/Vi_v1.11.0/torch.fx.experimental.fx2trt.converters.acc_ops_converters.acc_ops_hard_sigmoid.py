@tensorrt_converter(acc_ops.hardsigmoid)
def acc_ops_hard_sigmoid(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"Hard sigmoid received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    return add_activation_layer(network, input_val, trt.ActivationType.HARD_SIGMOID, target, name, alpha=1 / 6, beta=0.5)
