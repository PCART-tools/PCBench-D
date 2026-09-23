@functools.cache
def get_global_cache_path_impl(global_cache_dir: str) -> Optional[Path]:
    return (
        Path(os.path.join(global_cache_dir, CacheBase.get_system()["hash"]))
        if global_cache_dir is not None
        else None
    )
