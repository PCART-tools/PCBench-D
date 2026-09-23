def get_packable_nontensor_arg_idxs(op: Callable) -> Optional[List[int]]:
    """
    Returns nontensor arg idxs which correspond to arguments which will need
    to be packed.
    """
    if op == F.conv2d:
        # stride, padding, dilation, groups
        return [3, 4, 5, 6]
    return None
