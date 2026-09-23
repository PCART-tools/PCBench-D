def mm_config_kwargs(device):
    if device == "cpu":
        return {
            "scale": 0.5,
            "exclude": _is_large_block_for_cpu,
        }
    return {}
