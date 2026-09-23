def get_packable_tensor_kwarg_names(op: Callable) -> Optional[List[str]]:
    """
    Returns tensor kwarg names which correspond to parameters which will
    need to be packed.
    """
    if op in (F.conv2d, F.linear):
        return ['weight', 'bias']
    return None
