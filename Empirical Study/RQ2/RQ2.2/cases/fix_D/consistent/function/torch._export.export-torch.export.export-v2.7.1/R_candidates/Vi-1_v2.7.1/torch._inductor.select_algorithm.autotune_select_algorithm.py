def autotune_select_algorithm(*args, **kwargs):
    global _ALGORITHM_SELECTOR_CACHE
    if _ALGORITHM_SELECTOR_CACHE is None:
        _ALGORITHM_SELECTOR_CACHE = AlgorithmSelectorCache()

    if "return_multi_template" not in kwargs:
        kwargs["return_multi_template"] = (
            torch._inductor.config.benchmark_epilogue_fusion
        )

    return _ALGORITHM_SELECTOR_CACHE(*args, **kwargs)
