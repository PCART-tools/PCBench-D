def triton_config(num_stages, num_warps, **kwargs):
    from triton import Config  # type: ignore[attr-defined]

    return Config(kwargs, num_stages=num_stages, num_warps=num_warps)
