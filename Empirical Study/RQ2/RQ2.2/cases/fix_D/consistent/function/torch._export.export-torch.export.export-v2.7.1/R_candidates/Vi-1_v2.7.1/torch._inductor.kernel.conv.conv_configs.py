def conv_configs(m, n, k, *, device_type, **kwargs):
    if device_type == "cpu":
        return filtered_configs(
            m,
            n,
            k,
            configs=platform_configs,
            scale=0.5,
            exclude=_is_large_block_for_cpu,
        )
    return filtered_configs(m, n, k, configs=platform_configs)
