@functools.lru_cache()
def logging_base_dir() -> str:
    meta_dir = os.getcwd()
    base_dir = os.path.join(meta_dir, "nightly", "log")
    os.makedirs(base_dir, exist_ok=True)
    return base_dir
