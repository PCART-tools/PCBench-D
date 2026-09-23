def bmm_configs(m, n, k, *, device_type):
    if device_type == "cpu":
        return mm_configs(m, n, k, scale=0.5, exclude=_is_large_block_for_cpu)
    return mm_configs(m, n, k)
