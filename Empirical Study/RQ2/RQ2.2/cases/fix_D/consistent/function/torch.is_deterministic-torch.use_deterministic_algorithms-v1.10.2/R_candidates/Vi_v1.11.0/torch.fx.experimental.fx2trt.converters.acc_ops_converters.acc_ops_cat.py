@tensorrt_converter(acc_ops.cat)
def acc_ops_cat(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    tensors = kwargs["tensors"]

    if any(not isinstance(t, TRTTensor) for t in tensors):  # type: ignore[union-attr]
        raise RuntimeError(
            f"cat received inputs {tensors} that is not part " "of the TensorRT region!"
        )

    layer = network.add_concatenation(inputs=tensors)
    layer.axis = cast(int, kwargs["dim"]) - (1 if network.has_implicit_batch_dimension else 0)
    set_layer_name(layer, target, name)
    return layer.get_output(0)
