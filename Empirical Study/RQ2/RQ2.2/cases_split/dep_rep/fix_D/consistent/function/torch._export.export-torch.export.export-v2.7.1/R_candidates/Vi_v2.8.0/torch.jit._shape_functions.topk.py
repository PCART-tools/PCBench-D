def topk(self: list[int], k: int, dim: int = -1) -> tuple[list[int], list[int]]:
    if len(self) == 0:
        result: list[int] = []
    else:
        assert k <= self[dim], (
            f"k ({k}) is too big for dimension {dim} of size {self[dim]}"
        )
        result = _copy(self)
        result[dim] = k
    return result, result
