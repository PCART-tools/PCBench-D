def cross_entropy_loss(
    self: list[int],
    target: list[int],
    weight: Optional[list[int]] = None,
    reduction: int = 1,
    ignore_index: int = -100,
    label_smoothing: float = 0.0,
) -> list[int]:
    result_shape = nll_loss_forward(self, target, weight, reduction)[0]
    return result_shape
