def linear(input: list[int], weight: list[int], bias: Optional[list[int]]):
    out = matmul(input, t(weight))
    if bias is not None:
        assert broadcast(bias, out) == out
    return out
