def remote_autograd_cache_default() -> Optional[bool]:
    if os.environ.get("TORCHINDUCTOR_AUTOGRAD_REMOTE_CACHE") == "1":
        return True
    if os.environ.get("TORCHINDUCTOR_AUTOGRAD_REMOTE_CACHE") == "0":
        return False
    return None
