def scaled_mm_options_device_tma(  # type: ignore[no-untyped-def]
    config,  # triton.Config
    sym_m: sympy.core.numbers.Integer,
    sym_n: sympy.core.numbers.Integer,
    sym_k: sympy.core.numbers.Integer,
    layout: Layout,
    scale_a: StorageBox,
    scale_b: StorageBox,
    use_fast_accum: bool,
) -> dict[str, Any]:
    even_k_symbolic = (
        sympy.gcd(sym_k, config.kwargs["BLOCK_K"]) == config.kwargs["BLOCK_K"]
    )

    size_a, size_b = scale_a.get_size(), scale_b.get_size()
    assert are_compatible_scales(size_a, size_b), (
        "Expect scale_a and scale_b to be either both scalars (including single-element tensors) "
        f"or 1-dimensional tensors with the same size. Got scale_a: {len(size_a)} and scale_b: {len(size_b)}."
    )
    return dict(
        GROUP_M=8,
        EVEN_K=even_k_symbolic,
        ACC_TYPE="tl.float32",
        USE_FAST_ACCUM=use_fast_accum,
        num_stages=config.num_stages,
        num_warps=config.num_warps,
        # tensor-wise scaling if scalar scales
        SCALING_ROWWISE=len(scale_a.get_size()) == 2,
        TMA_SIZE=TMA_DESCRIPTOR_SIZE,
        NUM_SMS=get_num_sms(),
        **config.kwargs,
    )
