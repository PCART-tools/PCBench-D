def mm_config_kwargs(device, exclude_condition, dtype_size=None):
    if device == "cpu":
        return {
            "scale": 0.5,
            "exclude": exclude_condition,
        }

    if dtype_size and inductor_config.max_autotune_gemm_search_space == "EXHAUSTIVE":
        return {
            "dtype_size": dtype_size,
        }
    return {}
