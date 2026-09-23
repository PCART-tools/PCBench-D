def get_func_output_dtype_type(
    seen_op_info: SeenOpInfo,
) -> FuncOutputDTypeType:
    if seen_op_info.type_is_module:
        if seen_op_info.type in module_types_supported_by_quantization_preserves_dtype:
            return FuncOutputDTypeType.DTYPE_EQUALS_INPUT_DTYPE

    # check for ops which need packed weights but the weights are
    # coming from another function
    if not seen_op_info.op_packing_only_uses_module_attributes:
        return FuncOutputDTypeType.DTYPE_DEFAULT_BC_UNSUPPORTED_SYNTAX

    args = seen_op_info.input_tensor_infos
    if seen_op_info.type in functions_supported_by_quantization_preserves_dtype:
        return FuncOutputDTypeType.DTYPE_EQUALS_INPUT_DTYPE
    elif seen_op_info.type in add_and_mul_ops and len(args) > 0 and \
            args[0] is not None and \
            args[0].orig_dtype in (torch.int32, torch.int64):
        # binary ops with torch.int arguments do not support quantization
        return FuncOutputDTypeType.DTYPE_EQUALS_INPUT_DTYPE
    elif seen_op_info.type == torch.cat and len(args) > 0 and \
            args[0] is not None and \
            args[0].orig_dtype in (torch.int32, torch.int64):
        # TODO(before land): do we still need this branch?
        return FuncOutputDTypeType.DTYPE_EQUALS_INPUT_DTYPE

    return FuncOutputDTypeType.DTYPE_DEPENDS_ON_QCONFIG
