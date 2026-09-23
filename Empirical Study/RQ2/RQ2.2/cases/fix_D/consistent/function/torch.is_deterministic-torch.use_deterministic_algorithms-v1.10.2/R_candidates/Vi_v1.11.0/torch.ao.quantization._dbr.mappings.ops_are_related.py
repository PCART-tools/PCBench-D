def ops_are_related(
    cur_op: Callable,
    expected_op_type: Callable,
    type_is_module: bool,
) -> bool:
    # if isinstance(cur_op, torch.nn.Module):
    if type_is_module:
        cur_op = type(cur_op)
    return cur_op == expected_op_type or \
        (cur_op, expected_op_type) in a_related_to_b
