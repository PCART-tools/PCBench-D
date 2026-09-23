def movedim(
    input: TensorLikeType,
    source: Union[int, DimsSequenceType],
    destination: Union[int, DimsSequenceType],
) -> TensorLikeType:
    """
    Reference implementation of torch.movedim
    """
    if type(source) is int:
        source = (source,)
    if type(destination) is int:
        destination = (destination,)

    # Converts to list to produce a compatible error message with core PyTorch,
    # which prints sequences in square brackets.
    torch._check(
        len(source) == len(destination),  # type: ignore[arg-type]
        lambda: (
            "movedim: Invalid source or destination dims: source "  # type: ignore[arg-type]
            f"({list(source)} dims) should contain the same number "  # type: ignore[arg-type]
            f"of dims as destination ({list(destination)} dims)"  # type: ignore[arg-type]
        ),
    )

    rank = input.ndim
    ss = tuple(utils.canonicalize_dims(rank=rank, indices=source))  # type: ignore[arg-type]
    ds = tuple(utils.canonicalize_dims(rank=rank, indices=destination))  # type: ignore[arg-type]

    sss = set(ss)
    dss = set(ds)

    # See above on why this converts to list in error messages.
    torch._check(
        len(ss) == len(sss),
        lambda: f"movedim: repeated dim in `source` ({list(source)})",  # type: ignore[arg-type]
    )
    torch._check(
        len(ds) == len(dss),
        lambda: f"movedim: repeated dim in `destination` ({list(destination)})",  # type: ignore[arg-type]
    )

    m = dict(zip(ds, ss))
    dims = []
    si = 0  # source index
    for di in range(rank):
        # check if the destination index is in the mapping
        s = m.get(di)
        if s is not None:
            # insert source index if found
            dims.append(s)
        else:
            # insert source index sequentially, skipping indices from the mapping
            while si in sss:
                si += 1
            dims.append(si)
            si += 1

    result = torch.permute(input, tuple(dims))

    return result
