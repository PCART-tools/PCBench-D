def get_input_observed_arg_idxs(
    op_type: Callable,
    op_type_is_module: bool,
) -> Optional[List[int]]:
    if op_type_is_module:
        # TODO(future PR): handle RNNs
        return [0]
    elif op_type == F.conv2d:
        return [0, 1]
    elif op_type == F.linear:
        return [0, 1]
    # None means "observe all Tensor args"
    return None
