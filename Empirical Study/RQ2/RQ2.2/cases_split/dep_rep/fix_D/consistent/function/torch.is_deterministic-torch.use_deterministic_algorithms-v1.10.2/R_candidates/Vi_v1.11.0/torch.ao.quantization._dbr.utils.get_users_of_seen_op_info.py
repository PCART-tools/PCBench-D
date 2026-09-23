def get_users_of_seen_op_info(
    idx_to_seen_op_info: Dict[int, SeenOpInfo],
    cur_seen_op_info: SeenOpInfo,
) -> List[SeenOpInfo]:
    """
    Input: cur_seen_op_info
    Output: list of all seen_op_infos which use the output of the cur_seen_op_info,
    """
    if len(cur_seen_op_info.output_tensor_infos) != 1:
        return []
    output_tensor_id = cur_seen_op_info.output_tensor_infos[0].id
    results = []
    for idx, seen_op_info in idx_to_seen_op_info.items():
        for input_tensor_info in seen_op_info.input_tensor_infos:
            if input_tensor_info is not None:
                if output_tensor_id == input_tensor_info.id:
                    results.append(seen_op_info)
    return results
