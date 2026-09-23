def normalize_gm(gm_str: str) -> str:
    # strip comments as comments have path to files which may differ from
    # system to system.
    return remove_trailing_space(strip_comment(gm_str))
