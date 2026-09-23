def add_activation_layer(
    network: TRTNetwork,
    input_val: TRTTensor,
    operation_type: trt.ActivationType,
    target: Target,
    name: str,
    alpha: Optional[Any] = None,
    beta: Optional[Any] = None,
) -> TRTTensor:
    """
    Add a TensorRT Activation layer to `network`.

    Args:
        network (TRTNetwork): TensorRT network object.
        input_val (TRTTensor): Input to the activation op.
            Must be a TensorRT tensor.
        op_type (trt.ElementWiseOperation): Type of the TensorRT activation
            operation.
        target (Target): Target of fx node.
        name (str): The name we want to assign to the created TensorRT layer.
        alpha (Optional[Any]): If not None, we will use it to set the alpha
            attribute of the created TensorRT activation layer.
        beta (Optional[Any]): If not None, we will use it to set the beta
            attribute of the created TensorRT activation layer.

    Returns:
        The output of TensorRT Activation layer.
    """
    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"{operation_type} received input {input_val} that is not part "
            "of the TensorRT region!"
        )
    layer = network.add_activation(input_val, operation_type)
    if alpha is not None:
        layer.alpha = alpha
    if beta is not None:
        layer.beta = beta
    set_layer_name(layer, target, name)
    return layer.get_output(0)
