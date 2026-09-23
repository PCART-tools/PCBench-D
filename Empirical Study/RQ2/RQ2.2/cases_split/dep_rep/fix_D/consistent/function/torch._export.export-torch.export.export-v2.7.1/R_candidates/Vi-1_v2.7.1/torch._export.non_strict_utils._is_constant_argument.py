def _is_constant_argument(t):
    return t is None or isinstance(t, (int, float, bool, str))
