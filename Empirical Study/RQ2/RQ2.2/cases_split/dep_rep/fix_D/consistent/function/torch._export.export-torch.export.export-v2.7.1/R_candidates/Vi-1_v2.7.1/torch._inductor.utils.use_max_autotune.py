def use_max_autotune() -> bool:
    return (
        config.max_autotune or config.max_autotune_gemm or config.search_autotune_cache
    )
