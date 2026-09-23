def searchsorted(
    a: ArrayLike, v: ArrayLike, side="left", sorter: Optional[ArrayLike] = None
):
    if a.dtype.is_complex:
        raise NotImplementedError(f"searchsorted with dtype={a.dtype}")

    return torch.searchsorted(a, v, side=side, sorter=sorter)
