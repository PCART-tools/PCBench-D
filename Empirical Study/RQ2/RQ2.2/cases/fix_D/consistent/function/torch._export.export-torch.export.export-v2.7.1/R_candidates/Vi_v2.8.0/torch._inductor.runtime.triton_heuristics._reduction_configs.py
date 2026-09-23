def _reduction_configs(
    *, size_hints: dict[str, int], inductor_meta: dict[str, Any]
) -> list[Config]:
    reduction_hint = inductor_meta.get("reduction_hint", None)

    # Convert reductions to 1D, to simplify heuristics.
    rnumel = get_total_reduction_numel(size_hints)

    register_intensive = False
    MAX_R0_BLOCK = 2048
    if (
        size_hints["x"] >= 1024
        and inductor_meta.get("num_load", 0) + inductor_meta.get("num_reduction", 0)
        >= 10
    ):
        # A heuristics to reduce R0_BLOCK if a kernel potentially need many registers.
        # Consider load and reduction since load need move data into registers and
        # reduction needs an accumulator.
        #
        # The magic numbers are a bit arbitrary.
        #
        # We cannot rely on dynamically scaling down R0_BLOCK later, since sometimes
        # triton makes it to use less registers with worse perf. Check:
        # https://github.com/pytorch/pytorch/issues/126463
        #
        # The heuristic is a very simple one since registers can be reused. But
        # hopefully it can be a good enough indicator.
        MAX_R0_BLOCK = 1024
        register_intensive = True

    def make_config(x, r, num_warps=None, num_stages=1, register_intensive=False):
        # For 3D case with tiling scores, create an adapted version
        if "y" in size_hints:
            assert "tiling_scores" in inductor_meta
            return adapt_config_for_tiling(
                size_hints,
                inductor_meta["tiling_scores"],
                x,
                r,
                num_warps=num_warps,
                num_stages=num_stages,
                register_intensive=register_intensive,
            )
        else:
            # For other cases, use the original function
            return triton_config_reduction(
                size_hints,
                x,
                r,
                num_warps=num_warps,
                num_stages=num_stages,
                register_intensive=register_intensive,
            )

    contiguous_config = make_config(
        1,
        min(rnumel, MAX_R0_BLOCK),
        register_intensive=register_intensive,
    )
    outer_config = make_config(64, 8, register_intensive=register_intensive)
    tiny_config = make_config(
        2 * (256 // rnumel) if rnumel <= 256 else 1,
        min(rnumel, MAX_R0_BLOCK),
        register_intensive=register_intensive,
    )
    # For 3d tiling, default to more autotuning initially
    if "y" in size_hints:
        pass
    elif inductor_meta.get("max_autotune") or inductor_meta.get(
        "max_autotune_pointwise"
    ):
        pass  # skip all these cases
    elif reduction_hint == ReductionHint.INNER:
        return [contiguous_config]
    elif reduction_hint == ReductionHint.OUTER:
        return [outer_config]
    elif reduction_hint == ReductionHint.OUTER_TINY:
        return [tiny_config]
    if disable_pointwise_autotuning(inductor_meta):
        return [make_config(32, 128)]
    return [
        contiguous_config,
        outer_config,
        tiny_config,
        make_config(64, 64),
        make_config(8, 512),
        # halve the XBLOCK/Rn_BLOCK compared to outer_config
        # TODO: this may only be beneficial when each iteration of the reduction
        # is quite heavy. E.g. https://gist.github.com/shunting314/189a8ef69f90db9d614a823385147a72
        make_config(64, 4, num_warps=8),
    ]
