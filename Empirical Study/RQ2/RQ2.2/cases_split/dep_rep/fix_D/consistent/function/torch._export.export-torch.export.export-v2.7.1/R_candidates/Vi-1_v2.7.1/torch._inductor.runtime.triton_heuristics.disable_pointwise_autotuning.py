def disable_pointwise_autotuning(inductor_meta):
    # Autotuning can give different benchmarking results from run to run, and
    # therefore we disable autotuning when use_deterministic flag is on.
    if inductor_meta.get("are_deterministic_algorithms_enabled"):
        return True
    return not inductor_meta.get("autotune_pointwise", True)
