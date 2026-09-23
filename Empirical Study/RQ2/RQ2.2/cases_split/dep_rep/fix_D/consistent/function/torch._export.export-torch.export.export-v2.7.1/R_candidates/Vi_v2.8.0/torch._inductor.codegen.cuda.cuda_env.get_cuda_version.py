@clear_on_fresh_cache
@functools.lru_cache(1)
def get_cuda_version() -> Optional[str]:
    try:
        cuda_version = config.cuda.version
        if cuda_version is None:
            cuda_version = torch.version.cuda
        return cuda_version
    except Exception as e:
        log.error("Error getting cuda version: %s", e)
        return None
