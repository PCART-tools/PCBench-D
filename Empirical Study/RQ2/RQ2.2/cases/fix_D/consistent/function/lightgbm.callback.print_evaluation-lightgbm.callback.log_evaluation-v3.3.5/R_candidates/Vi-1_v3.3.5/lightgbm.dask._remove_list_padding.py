def _remove_list_padding(*args: Any) -> List[List[Any]]:
    return [[z for z in arg if z is not None] for arg in args]
