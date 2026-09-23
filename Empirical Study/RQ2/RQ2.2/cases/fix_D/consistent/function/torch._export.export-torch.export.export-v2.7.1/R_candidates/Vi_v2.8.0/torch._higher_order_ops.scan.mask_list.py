def mask_list(
    mask: list[bool], inp: list[Any], other: Optional[list[Any]] = None
) -> list[Any]:
    # Masks elements on an `inp` list.
    # If other is None, then the elements of the `inp` list where the mask is False are removed
    # If other is not None, then the elements of the `inp` list where the mask is False are
    # replaced with the elements of the `other` list
    assert len(mask) == len(
        inp
    ), "The length of the mask needs to be identical to the length of the input"
    if other is not None:
        assert len(inp) == len(
            other
        ), "If an input and an other list is provided, they need to have the same length"
        return [i if m else o for m, i, o in zip(mask, inp, other)]
    else:
        return [i for m, i in zip(mask, inp) if m]
