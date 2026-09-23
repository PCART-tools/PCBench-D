def get_weight_arg_idx(op: Callable) -> Optional[int]:
    if op == F.conv2d:
        return 1
    elif op == F.linear:
        return 1
    return None
