def _persistent_reduction_configs(
    size_hints,
    reduction_hint=False,
    inductor_meta=None,
):
    xnumel = size_hints["x"]
    rnumel = get_total_reduction_numel(size_hints)

    configs = [
        triton_config_reduction(size_hints, xblock, rnumel, register_intensive=True)
        for xblock in (1, 8, 32, 128)
        if xblock == 1 or (rnumel * xblock <= 4096 and xblock <= xnumel)
    ]

    # TODO(jansel): we should be able to improve these heuristics
    if reduction_hint == ReductionHint.INNER and rnumel >= 256:
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
