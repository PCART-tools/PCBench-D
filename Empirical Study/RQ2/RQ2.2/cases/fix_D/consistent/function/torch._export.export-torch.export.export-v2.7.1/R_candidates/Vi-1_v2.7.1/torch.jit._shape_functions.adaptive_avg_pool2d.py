def adaptive_avg_pool2d(self: list[int], out: list[int]):
    assert len(out) == 2
    assert len(self) == 3 or len(self) == 4
    for i in range(1, len(self)):
        assert self[i] != 0

    shape: list[int] = []
    for i in range(0, len(self) - 2):
        shape.append(self[i])
    for elem in out:
        shape.append(elem)
    return shape
