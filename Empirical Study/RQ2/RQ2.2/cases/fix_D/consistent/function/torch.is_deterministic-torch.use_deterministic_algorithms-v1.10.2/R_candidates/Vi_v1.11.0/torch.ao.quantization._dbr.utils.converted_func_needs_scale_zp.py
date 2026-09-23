def converted_func_needs_scale_zp(seen_op_info: SeenOpInfo) -> bool:
    op_type = seen_op_info.type
    is_module = isinstance(op_type, type(torch.nn.Module))
    if is_module:
        return False
    if seen_op_info.qconfig is None:
        return False
    if op_type in add_and_mul_ops:
        # check if both arguments are tensors
        inputs = seen_op_info.input_tensor_infos
        both_args_tensors = len(inputs) == 2 and inputs[0] is not None and \
            inputs[1] is not None
        # disable quantization for torch.mul with int tensor arguments
        first_dtype_is_not_int = len(inputs) > 0 and \
            inputs[0] is not None and \
            inputs[0].inf_dtype not in (torch.int32, torch.int64)
        return both_args_tensors and first_dtype_is_not_int
    elif op_type == torch.cat:
        inputs = seen_op_info.input_tensor_infos
        first_dtype_is_not_int = len(inputs) > 0 and \
            inputs[0] is not None and \
            inputs[0].inf_dtype not in (torch.int32, torch.int64)
        return first_dtype_is_not_int
    elif op_type in (F.conv2d, F.linear):
        outputs = seen_op_info.output_tensor_infos
        is_int8 = outputs[0].inf_dtype == torch.quint8
        return is_int8
    return False
