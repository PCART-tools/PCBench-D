def _get_type_from_tensor(
    tensor: torch.Tensor
    | torch.SymBool
    | torch.SymInt
    | torch.SymFloat
    | Sequence[torch.Tensor],
) -> ir.TypeProtocol:
    if isinstance(tensor, torch.Tensor):
        return ir.TensorType(_torch_dtype_to_onnx_compatible_dtype(tensor.dtype))
    if isinstance(tensor, torch.SymBool):
        return ir.TensorType(ir.DataType.BOOL)
    if isinstance(tensor, torch.SymInt):
        return ir.TensorType(ir.DataType.INT64)
    if isinstance(tensor, torch.SymFloat):
        return ir.TensorType(ir.DataType.FLOAT)

    # Handle sequences
    first_tensor = next((item for item in tensor if item is not None), None)
    if first_tensor is None:
        return ir.SequenceType(ir.TensorType(ir.DataType.UNDEFINED))
    return ir.SequenceType(
        ir.TensorType(_torch_dtype_to_onnx_compatible_dtype(first_tensor.dtype))
    )
