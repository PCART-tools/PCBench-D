def batch_norm(
    input: list[int],
    weight: Optional[list[int]],
    bias: Optional[list[int]],
    running_mean: Optional[list[int]],
    running_var: Optional[list[int]],
    training: bool,
    momentum: float,
    eps: float,
    cudnn_enabled: bool,
):
    out: list[int] = []
    for elem in input:
        out.append(elem)
    return out
