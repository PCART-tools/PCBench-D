def choose(
    a: ArrayLike,
    choices: Sequence[ArrayLike],
    out: Optional[OutArray] = None,
    mode: NotImplementedType = "raise",
):
    # First, broadcast elements of `choices`
    choices = torch.stack(torch.broadcast_tensors(*choices))

    # Use an analog of `gather(choices, 0, a)` which broadcasts `choices` vs `a`:
    # (taken from https://github.com/pytorch/pytorch/issues/9407#issuecomment-1427907939)
    idx_list = [
        torch.arange(dim).view((1,) * i + (dim,) + (1,) * (choices.ndim - i - 1))
        for i, dim in enumerate(choices.shape)
    ]

    idx_list[0] = a
    return choices[idx_list].squeeze(0)
