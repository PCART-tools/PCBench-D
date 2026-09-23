def _list_with_default(out_size: List[int], defaults: List[int]) -> List[int]:
    if isinstance(out_size, int):
        return out_size
    if len(defaults) <= len(out_size):
        raise ValueError(
            "Input dimension should be at least {}".format(len(out_size) + 1)
        )
    return [
        v if v is not None else d for v, d in zip(out_size, defaults[-len(out_size) :])
    ]
