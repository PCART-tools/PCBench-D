@functools.lru_cache(None)
def lazy_register_extern_choice(fn):
    return ExternKernelChoice(fn)
