def get_quantized_op(
    seen_op_info: SeenOpInfo,
) -> Optional[Callable]:
    """
    Given a `seen_op_info`, returns the quantized version of the seen function.
    If the `seen_op_info` corresponds to a module, returns `None`.
    If the function does need quantizing, returns `None`.
    """
    op_type = seen_op_info.type
    is_module = isinstance(op_type, type(torch.nn.Module))
    if is_module:
        return None
    if seen_op_info.output_tensor_infos[0].inf_dtype != torch.quint8:
        return None

    if (
        (op_type in add_and_mul_ops or op_type == torch.cat) and
        seen_op_info.input_tensor_infos[0] is not None and
        seen_op_info.input_tensor_infos[0].inf_dtype in (torch.int32, torch.int64)
    ):
        # handle torch.mul with int tensor arguments
        return None
    elif op_type in fp32_to_int8_fun_mapping:
        return fp32_to_int8_fun_mapping[op_type]
    return None
