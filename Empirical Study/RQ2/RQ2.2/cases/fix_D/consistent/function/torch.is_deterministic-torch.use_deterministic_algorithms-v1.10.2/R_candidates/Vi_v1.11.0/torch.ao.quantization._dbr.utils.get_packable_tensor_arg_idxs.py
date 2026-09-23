def get_packable_tensor_arg_idxs(op: Callable) -> Optional[List[int]]:
    """
    Returns tensor arg idxs which correspond to parameters which will need
    to be packed.
    """
    if op == F.conv2d:
        return [1, 2]
    elif op == F.linear:
        return [1, 2]
    return None
