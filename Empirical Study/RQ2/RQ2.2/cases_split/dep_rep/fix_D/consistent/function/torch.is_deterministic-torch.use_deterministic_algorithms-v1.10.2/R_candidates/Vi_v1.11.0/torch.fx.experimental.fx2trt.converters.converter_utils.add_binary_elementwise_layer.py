def add_binary_elementwise_layer(
    network: TRTNetwork,
    lhs_val: Union[int, float, TRTTensor, torch.Tensor],
    rhs_val: Union[int, float, TRTTensor, torch.Tensor],
    op_type: trt.ElementWiseOperation,
    target: Target,
    name: str
) -> TRTTensor:
    """
    This function adds a TensorRT elementwise layer. We allow both operands to be
    constant (not a trt tensor) because in implicit batch dimension mode, we could
    introduce constant via .size() op. Other scenario should be const folded first.
    If any operand is not a trt tensor, we make it a trt constant layer which has
    the same type as the other trt tensor. Then we broadcast these two inputs to
    have the same number of dimensions.

    Limitation:
        If we are using implicit batch dim mode, the operand that is not a trt
    tensor are not allowed to have larger ranks than the trt tensor operand.

    Args:
        network (TRTNetwork): TensorRT network object.
        lhs_val (TRTTensor): Left operand of the binary operation. Could
            be a TensorRT tensor, a PyTorch tensor or a simple value.
        rhs_val (TRTTensor): Right operand of the binary operation. Similar
            to lhs_val.
        op_type (trt.ElementWiseOperation): Type of the TensorRT elementwise binary operation.
        target (Target): Target of fx node.
        name (str): The name we want to assign to the created TensorRT layer.

    Returns:
        The output of TensorRT Elementwise layer.
    """
    dtype = None
    is_lhs_trt_tensor = False
    is_rhs_trt_tensor = False
    if isinstance(lhs_val, TRTTensor):
        dtype = torch_dtype_from_trt(lhs_val.dtype)
        is_lhs_trt_tensor = True
    if isinstance(rhs_val, TRTTensor):
        dtype = torch_dtype_from_trt(rhs_val.dtype)
        is_rhs_trt_tensor = True
    if not is_lhs_trt_tensor and not is_rhs_trt_tensor:
        warnings.warn(f"Both operands of the binary elementwise op {name} "
                      "are constant. In this case, please consider constant fold the model first.")
        return get_python_op_from_trt_elementwise_op(op_type)(lhs_val, rhs_val)

    lhs_val = get_trt_tensor(network, lhs_val, f"{name}_lhs", dtype)
    rhs_val = get_trt_tensor(network, rhs_val, f"{name}_rhs", dtype)

    # Check the limitation in the doc string.
    if network.has_implicit_batch_dimension:
        if is_lhs_trt_tensor and not is_rhs_trt_tensor:
            assert len(lhs_val.shape) >= len(rhs_val.shape), f"{lhs_val.shape} >= {rhs_val.shape}"
        elif not is_lhs_trt_tensor and is_rhs_trt_tensor:
            assert len(rhs_val.shape) >= len(lhs_val.shape), f"{rhs_val.shape} >= {lhs_val.shape}"

    lhs_val, rhs_val = broadcast(
        network, lhs_val, rhs_val, f"{name}_lhs", f"{name}_rhs"
    )
    layer = network.add_elementwise(lhs_val, rhs_val, op_type)
    set_layer_name(layer, target, name)
    return layer.get_output(0)
