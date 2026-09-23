def scaled_mm_options(  # type: ignore[no-untyped-def]
    config,  # triton.Config
    sym_m: sympy.core.numbers.Integer,
    sym_n: sympy.core.numbers.Integer,
    sym_k: sympy.core.numbers.Integer,
    layout: Layout,
    scale_a,
    scale_b,
    use_fast_accum: bool,
    device_tma: bool = False,
) -> dict[str, Any]:
    def are_compatible_scales(size_a, size_b) -> bool:
        # Same sized scales are compatible
        if len(size_a) == len(size_b):
            return True

        # Both need to be scalars or len(1) tensors
        if len(size_a) <= 1 and len(size_b) <= 1:
            return True

        return False

    size_a, size_b = scale_a.get_size(), scale_b.get_size()
    assert are_compatible_scales(size_a, size_b), (
        "Expect scale_a and scale_b to be either both scalars (including single-element tensors) "
        f"or 1-dimensional tensors with the same size. Got scale_a: {len(size_a)} and scale_b: {len(size_b)}."
    )

    mm_template_options = mm_options(config, sym_m, sym_n, sym_k, layout)

    mm_template_options["ACC_TYPE"] = "tl.float32"
    mm_template_options["USE_FAST_ACCUM"] = use_fast_accum
    mm_template_options["SCALING_ROWWISE"] = len(size_a) == 2

    if device_tma:
        mm_template_options["TMA_SIZE"] = TMA_DESCRIPTOR_SIZE
        mm_template_options["NUM_SMS"] = get_num_sms()

    mm_template_options.update(tma_options())

    return mm_template_options
