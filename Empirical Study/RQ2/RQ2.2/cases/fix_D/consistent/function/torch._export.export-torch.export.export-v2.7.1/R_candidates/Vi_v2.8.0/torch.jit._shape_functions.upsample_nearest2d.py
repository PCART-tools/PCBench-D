def upsample_nearest2d(
    input: list[int],
    output_size: Optional[list[int]],
    scale_factors: Optional[list[float]],
):
    out: list[int] = []
    out.append(input[0])
    out.append(input[1])

    if scale_factors is None and output_size is None:
        assert 0, "Either output_size or scale_factors must be presented"

    if output_size is not None:
        assert scale_factors is None, (
            "Must specify exactly one of output_size and scale_factors"
        )
        assert len(output_size) == 2
        out.append(output_size[0])
        out.append(output_size[1])

    if scale_factors is not None:
        assert output_size is None, (
            "Must specify exactly one of output_size and scale_factors"
        )
        assert len(scale_factors) == 2
        out.append(int(input[2] * scale_factors[0]))
        out.append(int(input[3] * scale_factors[1]))

    return out
