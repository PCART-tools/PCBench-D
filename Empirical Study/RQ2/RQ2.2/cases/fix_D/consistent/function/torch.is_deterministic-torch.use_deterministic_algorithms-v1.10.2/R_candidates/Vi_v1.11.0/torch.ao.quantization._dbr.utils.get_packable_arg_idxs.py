def get_packable_arg_idxs(op: Callable) -> Optional[List[int]]:
    if op == F.conv2d:
        # weight, bias, stride, padding, dilation, groups
        return [1, 2, 3, 4, 5, 6]
    elif op == F.linear:
        # weight, bias
        return [1, 2]
    return None
