def _register_builtin(fn, op):
    _get_builtin_table()[id(fn)] = op
