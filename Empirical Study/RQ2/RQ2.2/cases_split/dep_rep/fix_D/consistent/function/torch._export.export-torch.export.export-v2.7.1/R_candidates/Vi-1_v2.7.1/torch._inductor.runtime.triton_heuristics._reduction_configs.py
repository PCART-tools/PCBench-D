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

    contiguous_config = triton_config_reduction(
        size_hints,
        1,
        rnumel if 256 <= rnumel < MAX_R0_BLOCK else MAX_R0_BLOCK,
        register_intensive=register_intensive,
    )
    outer_config = triton_config_reduction(
        size_hints, 64, 8, register_intensive=register_intensive
    )
    tiny_config = triton_config_reduction(
        size_hints,
        2 * (256 // rnumel) if rnumel <= 256 else 1,
        min(rnumel, MAX_R0_BLOCK),
        register_intensive=register_intensive,
    )
    if inductor_meta.get("max_autotune") or inductor_meta.get("max_autotune_pointwise"):
        pass  # skip all these cases
    elif reduction_hint == ReductionHint.INNER:
        return [contiguous_config]
    elif reduction_hint == ReductionHint.OUTER:
        return [outer_config]
    elif reduction_hint == ReductionHint.OUTER_TINY:
        return [tiny_config]
    if disable_pointwise_autotuning(inductor_meta):
        return [triton_config_reduction(size_hints, 32, 128)]
    return [
        contiguous_config,
        outer_config,
        tiny_config,
        triton_config_reduction(size_hints, 64, 64),
        triton_config_reduction(size_hints, 8, 512),
        # halve the XBLOCK/Rn_BLOCK compared to outer_config
        # TODO: this may only be beneficial when each iteration of the reduction
        # is quite heavy. E.g. https://gist.github.com/shunting314/189a8ef69f90db9d614a823385147a72
        triton_config_reduction(size_hints, 64, 4, num_warps=8),
    ]
