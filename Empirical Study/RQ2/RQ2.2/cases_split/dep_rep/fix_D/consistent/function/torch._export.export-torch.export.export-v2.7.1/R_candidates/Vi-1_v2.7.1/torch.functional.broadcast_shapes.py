def broadcast_shapes(*shapes):
    r"""broadcast_shapes(*shapes) -> Size

    Similar to :func:`broadcast_tensors` but for shapes.

    This is equivalent to
    ``torch.broadcast_tensors(*map(torch.empty, shapes))[0].shape``
    but avoids the need create to intermediate tensors. This is useful for
    broadcasting tensors of common batch shape but different rightmost shape,
    e.g. to broadcast mean vectors with covariance matrices.

    Example::

        >>> torch.broadcast_shapes((2,), (3, 1), (1, 1, 1))
        torch.Size([1, 3, 2])

    Args:
        \*shapes (torch.Size): Shapes of tensors.

    Returns:
        shape (torch.Size): A shape compatible with all input shapes.

    Raises:
        RuntimeError: If shapes are incompatible.
    """
    # This wrapper exists to support variadic args.
    # TODO Move this to C++ once the jit has better support for torch.Size.
    if not torch.jit.is_tracing():
        max_len = 0
        for shape in shapes:
            if isinstance(shape, (int, torch.SymInt)):
                if max_len < 1:
                    max_len = 1
            elif isinstance(shape, (tuple, list)):
                s = len(shape)
                if max_len < s:
                    max_len = s
        result = [1] * max_len

        from torch.fx.experimental.symbolic_shapes import (
            guard_size_oblivious,
            is_nested_int,
        )

        for shape in shapes:
            if isinstance(shape, (int, torch.SymInt)):
                shape = (shape,)
            if isinstance(shape, (tuple, list)):
                for i in range(-1, -1 - len(shape), -1):
                    if shape[i] < 0:
                        raise RuntimeError(
                            f"Trying to create tensor with negative dimension ({shape[i]}): ({shape[i]})"
                        )

                    # NB: handle nested ints specially to avoid invalid guarding on Ne(j0, 1).
                    if is_nested_int(shape[i]):
                        # Broadcasting is allowed for (j0, 1) or (j0, j0);
                        # not (j0, j1), (j0, 5), etc.
                        if is_nested_int(result[i]) and guard_size_oblivious(
                            shape[i] == result[i]
                        ):
                            continue
                    else:
                        # NB: result is initialized to 1 so this is effectively an
                        # equals one test
                        if guard_size_oblivious(shape[i] == 1) or guard_size_oblivious(
                            shape[i] == result[i]
                        ):
                            continue

                    if result[i] != 1:
                        raise RuntimeError(
                            "Shape mismatch: objects cannot be broadcast to a single shape"
                        )
                    result[i] = shape[i]
            else:
                raise RuntimeError(
                    "Input shapes should be of type ints, a tuple of ints, or a list of ints, got ",
                    shape,
                )
        return torch.Size(result)
    else:
        # with implementation above, torch.jit.trace hardcodes the sizes which makes subsequent replays fail
        with torch.no_grad():
            scalar = torch.zeros((), device="cpu")
            tensors = [scalar.expand(shape) for shape in shapes]
            tensors = broadcast_tensors(*tensors)
            return tensors[0].shape
