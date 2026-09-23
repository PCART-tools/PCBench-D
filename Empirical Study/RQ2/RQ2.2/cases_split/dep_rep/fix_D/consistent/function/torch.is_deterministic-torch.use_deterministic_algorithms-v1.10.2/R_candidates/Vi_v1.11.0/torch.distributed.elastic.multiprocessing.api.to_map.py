def to_map(
    val_or_map: Union[Std, Dict[int, Std]], local_world_size: int
) -> Dict[int, Std]:
    """
    Certain APIs take redirect settings either as a single value (e.g. apply to all
    local ranks) or as an explicit user-provided mapping. This method is a convenience
    method that converts a value or mapping into a mapping.

    Example:

    ::

     to_map(Std.OUT, local_world_size=2) # returns: {0: Std.OUT, 1: Std.OUT}
     to_map({1: Std.OUT}, local_world_size=2) # returns: {0: Std.NONE, 1: Std.OUT}
     to_map({0: Std.OUT, 1: Std.OUT}, local_world_size=2) # returns: {0: Std.OUT, 1: Std.OUT}
    """
    if isinstance(val_or_map, Std):
        return {i: val_or_map for i in range(local_world_size)}
    else:
        map = {}
        for i in range(local_world_size):
            map[i] = val_or_map.get(i, Std.NONE)
        return map
