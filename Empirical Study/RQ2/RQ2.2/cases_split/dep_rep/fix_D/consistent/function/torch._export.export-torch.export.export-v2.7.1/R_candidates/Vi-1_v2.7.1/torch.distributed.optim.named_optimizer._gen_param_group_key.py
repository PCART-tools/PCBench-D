def _gen_param_group_key(param_keys: list[str]) -> str:
    """Concatenate all param keys as a unique indentifier for one param group."""
    return "/".join(sorted(param_keys))
