def t(self: list[int]):
    assert len(self) <= 2
    self_len = len(self)
    if self_len == 0:
        out: list[int] = []
        return out
    elif self_len == 1:
        return [self[0]]
    else:
        return [self[1], self[0]]
