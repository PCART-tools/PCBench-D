def get_producer_of_seen_op_info(
    idx_to_seen_op_info: Dict[int, SeenOpInfo],
    cur_seen_op_info: SeenOpInfo,
) -> Optional[SeenOpInfo]:
    """
    Input: cur_seen_op_info, all seen ops
    Output: the SeenOpInfo which created the input to the current SeenOpInfo
    """
    if cur_seen_op_info.input_tensor_infos[0] is None:
        return None
    input_tensor_id = cur_seen_op_info.input_tensor_infos[0].id
    for idx, seen_op_info in idx_to_seen_op_info.items():
        for output_tensor_info in seen_op_info.output_tensor_infos:
            if output_tensor_info is not None:
                if input_tensor_id == output_tensor_info.id:
                    return seen_op_info
    return None
