def _forward_from_src(src: str, globals: Dict[str, Any]):
    # avoid mutating the passed in dict
    globals_copy = globals.copy()
    _exec_with_source(src, globals_copy)
    forward_fn = globals_copy['forward']
    del globals_copy['forward']
    return forward_fn
