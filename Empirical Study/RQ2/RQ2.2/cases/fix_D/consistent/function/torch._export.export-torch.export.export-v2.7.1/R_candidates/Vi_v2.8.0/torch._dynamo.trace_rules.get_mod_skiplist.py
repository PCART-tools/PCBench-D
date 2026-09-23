@functools.cache
def get_mod_skiplist():
    skiplist = {
        _as_posix_path(_module_dir(torch) + m[len("torch.") :].replace(".", "/"))
        for m in MOD_SKIPLIST
    }
    return skiplist
