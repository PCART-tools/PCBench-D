def get_weight_argument_info(op: Callable) -> Optional[Tuple[int, str]]:
    if op in (F.linear, F.conv2d):
        return (1, 'weight')
    return None
