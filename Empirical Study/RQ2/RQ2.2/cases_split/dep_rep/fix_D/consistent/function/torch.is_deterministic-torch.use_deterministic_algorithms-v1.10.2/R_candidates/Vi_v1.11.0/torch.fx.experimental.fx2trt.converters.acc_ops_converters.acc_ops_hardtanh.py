@tensorrt_converter(acc_ops.hardtanh)
def acc_ops_hardtanh(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"hardtanh received input {input_val} that is not part "
                           "of the TensorRT region!")

    return add_activation_layer(
        network,
        input_val,
        trt.ActivationType.CLIP,
        target,
        name,
        alpha=kwargs["min_val"],
        beta=kwargs["max_val"],
    )
