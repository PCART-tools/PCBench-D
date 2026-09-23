def assert_nyi(cond, msg):
    if not cond:
        raise NotImplementedError(f"inductor does not support {msg}")
