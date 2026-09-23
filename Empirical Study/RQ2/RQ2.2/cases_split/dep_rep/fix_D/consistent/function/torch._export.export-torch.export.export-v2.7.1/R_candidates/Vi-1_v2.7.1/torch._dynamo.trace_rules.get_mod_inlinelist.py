@functools.lru_cache(None)
def get_mod_inlinelist():
    inlinelist = {
        _as_posix_path(_module_dir(torch) + m[len("torch.") :].replace(".", "/"))
        for m in MOD_INLINELIST
    }
    return inlinelist
