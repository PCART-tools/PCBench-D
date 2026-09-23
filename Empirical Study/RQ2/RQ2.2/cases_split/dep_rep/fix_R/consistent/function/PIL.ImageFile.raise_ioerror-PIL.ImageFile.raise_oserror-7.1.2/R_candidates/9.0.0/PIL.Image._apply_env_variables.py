def _apply_env_variables(env=None):
    if env is None:
        env = os.environ

    for var_name, setter in [
        ("PILLOW_ALIGNMENT", core.set_alignment),
        ("PILLOW_BLOCK_SIZE", core.set_block_size),
        ("PILLOW_BLOCKS_MAX", core.set_blocks_max),
    ]:
        if var_name not in env:
            continue

        var = env[var_name].lower()

        units = 1
        for postfix, mul in [("k", 1024), ("m", 1024 * 1024)]:
            if var.endswith(postfix):
                units = mul
                var = var[: -len(postfix)]

        try:
            var = int(var) * units
        except ValueError:
            warnings.warn(f"{var_name} is not int")
            continue

        try:
            setter(var)
        except ValueError as e:
            warnings.warn(f"{var_name}: {e}")
