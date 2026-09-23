def is_torch_inline_allowed(filename):
    return any(filename.startswith(d) for d in get_mod_inlinelist())
