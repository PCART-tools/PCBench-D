def _persistent_reduction_configs(
    size_hints,
    reduction_hint=False,
    inductor_meta=None,
):
    xnumel = size_hints["x"]
    rnumel = get_total_reduction_numel(size_hints)

    MAX_PERSISTENT_BLOCK_NUMEL = 4096

    if "y" not in size_hints:
        configs = [
            triton_config_reduction(size_hints, xblock, rnumel, register_intensive=True)
            for xblock in (1, 8, 32, 128)
            if xblock == 1
            or (rnumel * xblock <= MAX_PERSISTENT_BLOCK_NUMEL and xblock <= xnumel)
        ]
    else:
        configs = []
        assert "tiling_scores" in inductor_meta
        x_y_scores = {dim: inductor_meta["tiling_scores"][dim] for dim in ("x", "y")}
        for target_block_size in (1, 8, 32, 64, 128):
            if target_block_size * rnumel > MAX_PERSISTENT_BLOCK_NUMEL:
                continue

            block_sizes = match_target_block_product(
                size_hints, x_y_scores, target_block_size
            )
            configs.append(
                triton_config_tiled_reduction(
                    size_hints, block_sizes["x"], block_sizes["y"], rnumel
                )
            )

    # defer to more autotuning, initially
    if "y" in size_hints:
        pass
    # TODO(jansel): we should be able to improve these heuristics
    elif reduction_hint == ReductionHint.INNER and rnumel >= 256:
        configs = configs[:1]
    elif reduction_hint == ReductionHint.OUTER:
        configs = configs[-1:]
    elif reduction_hint == ReductionHint.OUTER_TINY:
        configs = [
            triton_config_reduction(
                size_hints,
                2 * (256 // rnumel) if rnumel <= 256 else 1,
                rnumel,
            )
        ]
    for c in configs:
        # we don't need Rn_BLOCK for persistent reduction
        for prefix in size_hints:
            if prefix_is_reduction(prefix):
                c.kwargs.pop(f"{prefix.upper()}BLOCK")

    if disable_pointwise_autotuning(inductor_meta):
        configs = configs[:1]

    return configs
