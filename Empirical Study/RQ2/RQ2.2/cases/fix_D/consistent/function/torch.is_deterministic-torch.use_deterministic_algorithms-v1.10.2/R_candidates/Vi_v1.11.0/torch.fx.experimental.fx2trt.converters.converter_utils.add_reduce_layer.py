def add_reduce_layer(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    operation_type: trt.ActivationType,
    name: str,
) -> TRTTensor:
    """
    Add a TensorRT Reduce layer to `network`.

    Args:
        network (TRTNetwork): TensorRT network object.
        target (Target): Target of fx node.
        args (Tuple[Argument, ...]): Args of the fx node.
        kwargs (Dict[str, Argument]): Kwargs of the fx node.
        operation_type (trt.ElementWiseOperation): Type of the TensorRT activation
            operation.
        name (str): The name we want to assign to the created TensorRT layer.

    Returns:
        The output of TensorRT Reduce layer.
    """
    input_val = kwargs["input"]
    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"{name} received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    # If dim is specified, then the op is reducing over certain dimensions.
    # Otherwise, it's reducing over all elements, which is only supported in
    # explicit batch dimension.
    if "dim" not in kwargs:
        assert (
            not network.has_implicit_batch_dimension
        ), f"We don't support reduce({name}) over all the elements if batch dim is implicit."
        dim = range(0, len(input_val.shape))
    else:
        dim = kwargs["dim"]  # type: ignore[assignment]

    keepdim = False if "keepdim" not in kwargs else kwargs["keepdim"]
    layer = network.add_reduce(
        input_val,
        operation_type,
        get_axes_for_reduce_op(dim, network.has_implicit_batch_dimension),
        keepdim,
    )
    set_layer_name(layer, target, name)
    return layer.get_output(0)
