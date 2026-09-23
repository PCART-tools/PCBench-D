def infer_size(shape: ShapeType, numel: int) -> tuple[int, ...]:
    """
    Infers the size of a dim with size -1, if it exists.
    Also checks that new shape is compatible with the number of elements.
    """
    dim = None
    newsize = 1
    for i, d in enumerate(shape):
        if d == -1:
            torch._check(dim is None, lambda: "only one dimension can be inferred")
            dim = i
        elif d >= 0:
            newsize *= d
        else:
            torch._check(False, lambda: f"invalid shape dimension {d}")
    if dim is None:
        torch._check(
            numel == newsize,
            lambda: f"shape '{list(shape)}' is invalid for input of size {numel}",
        )
    else:
        from torch.fx.experimental.symbolic_shapes import definitely_true

        torch._check(
            newsize != 0,
            lambda: (
                f"cannot reshape tensor of 0 elements into shape {list(shape)} because the "
                f"unspecified dimension size -1 can be any value and is ambiguous"
                if definitely_true(numel == 0)
                else f"shape '{list(shape)}' is invalid for input of size {numel}"
            ),
        )
        torch._check(
            numel % newsize == 0,
            lambda: f"shape '{list(shape)}' is invalid for input of size {numel}",
        )
        # Convert to list to produce a compatible error message with core
        # PyTorch, which prints sequences in square brackets.
        shape = list(shape)
        shape[dim] = numel // newsize
        # NB: This is pretty important when you have unbacked SymInts.
        # Suppose you have (i0, 12) resizing into (2, -1, 12).  The old
        # range for i0 is typically [2, inf], which means if you divide
        # by two the new range should be [1, inf].  But this is bad news
        # if you have an unbacked SymInt: we need to reapply the unsound
        # assumption that the size is >= 2.
        torch._check_is_size(shape[dim])
    return tuple(shape)
