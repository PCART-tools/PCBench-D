def get_func_output_obs_type(
    seen_op_info: SeenOpInfo,
) -> FuncOutputObsType:
    op_type = seen_op_info.type
    is_module = isinstance(op_type, type(torch.nn.Module))
    if is_module:
        return FuncOutputObsType.NONE

    if seen_op_info.qconfig is None:
        return FuncOutputObsType.NONE

    # check for ops which need packed weights but the weights are
    # coming from another function
    if not seen_op_info.op_packing_only_uses_module_attributes:
        return FuncOutputObsType.NONE

    if op_type in add_and_mul_ops:
        if (
            len(seen_op_info.input_tensor_infos) > 0 and
            seen_op_info.input_tensor_infos[0] is not None and
            seen_op_info.input_tensor_infos[0].inf_dtype in (torch.int32, torch.int64)
        ):
            # this is handling ops on dtypes such as torch.int
            return FuncOutputObsType.NONE
        elif (
            len(seen_op_info.input_tensor_infos) > 1 and
            seen_op_info.input_tensor_infos[1] is None
        ):
            return FuncOutputObsType.REUSES_FIRST_INPUT_OBS
    elif op_type in (torch.relu, F.relu):
        return FuncOutputObsType.NONE
    elif op_type == torch.cat:
        if (
            len(seen_op_info.input_tensor_infos) > 0 and
            seen_op_info.input_tensor_infos[0] is not None and
            seen_op_info.input_tensor_infos[0].inf_dtype in (torch.int32, torch.int64)
        ):
            return FuncOutputObsType.NONE
    return FuncOutputObsType.NEW_OBS
