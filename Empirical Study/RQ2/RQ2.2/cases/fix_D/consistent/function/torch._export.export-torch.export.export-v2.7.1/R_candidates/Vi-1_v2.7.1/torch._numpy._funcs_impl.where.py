def where(
    condition: ArrayLike,
    x: Optional[ArrayLikeOrScalar] = None,
    y: Optional[ArrayLikeOrScalar] = None,
    /,
):
    if (x is None) != (y is None):
        raise ValueError("either both or neither of x and y should be given")

    if condition.dtype != torch.bool:
        condition = condition.to(torch.bool)

    if x is None and y is None:
        result = torch.where(condition)
    else:
        result = torch.where(condition, x, y)
    return result
