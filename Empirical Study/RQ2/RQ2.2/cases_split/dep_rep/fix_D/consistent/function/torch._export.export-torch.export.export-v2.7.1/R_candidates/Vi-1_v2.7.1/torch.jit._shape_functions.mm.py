def mm(self: list[int], mat2: list[int]):
    assert len(self) == 2, "self must be a matrix"
    assert len(mat2) == 2, "mat2 must be a matrix"

    assert self[1] == mat2[0]
    return [self[0], mat2[1]]
