def add_binary_elementwise_layer(network, lhs_val, rhs_val, op_type, name):
    """
    This function adds a TensorRT elementwise layer. We only allow at most one
    operand to not be a trt tensor, otherwise, we should const fold it first.
    If any operand is not a trt tensor, we make it a trt constant layer which
    has the same type as the other trt tensor. Then we broadcast these two inputs
    to have the same number of dimensions.

    Limitation:
        If we are using implicit batch dim mode, the operand that is not a trt
    tensor are not allowed to have larger ranks than the trt tensor operand.

    Args:
        network: TensorRT network object.
        lhs_val: Left operand of the binary operation. Could be a TensorRT tensor,
            a PyTorch tensor or a simple value.
        rhs_val: Right operand of the binary operation. Similar to lhs_val.
        op_type: Type of the TensorRT elementwise binary operation.
        name: The name we want to assign to the created TensorRT layer.

    Returns:
        The output of TensorRT elementwise layer.
    """
    dtype = None
    is_lhs_trt_tensor = False
    is_rhs_trt_tensor = False
    if isinstance(lhs_val, trt.tensorrt.ITensor):
        dtype = torch_dtype_from_trt(lhs_val.dtype)
        is_lhs_trt_tensor = True
    if isinstance(rhs_val, trt.tensorrt.ITensor):
        dtype = torch_dtype_from_trt(rhs_val.dtype)
        is_rhs_trt_tensor = True
    if not is_lhs_trt_tensor and not is_rhs_trt_tensor:
        raise RuntimeError(f"Both operands of the binary elementwise op {name}"
                           "are constant. In this case, please consider constant fold the model first.")

    lhs_val = get_trt_tensor(network, lhs_val, f"{name}_lhs", dtype)
    rhs_val = get_trt_tensor(network, rhs_val, f"{name}_rhs", dtype)

    # Check the limitation in the doc string.
    if network.has_implicit_batch_dimension:
        if is_lhs_trt_tensor and not is_rhs_trt_tensor:
            assert len(lhs_val.shape) >= len(rhs_val.shape)
        elif not is_lhs_trt_tensor and is_rhs_trt_tensor:
            assert len(rhs_val.shape) >= len(lhs_val.shape)

    lhs_val, rhs_val = broadcast(
        network, lhs_val, rhs_val, f"{name}_lhs", f"{name}_rhs"
    )
    layer = network.add_elementwise(lhs_val, rhs_val, op_type)
    layer.name = name
    return layer.get_output(0)
