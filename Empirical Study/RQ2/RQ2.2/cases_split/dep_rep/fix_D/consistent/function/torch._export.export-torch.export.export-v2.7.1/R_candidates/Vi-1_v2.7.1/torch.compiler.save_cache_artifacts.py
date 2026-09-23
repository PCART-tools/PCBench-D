def save_cache_artifacts() -> Optional[tuple[bytes, "CacheInfo"]]:
    """
    Serializes all the cache artifacts that were created during the compilation

    Example:

    - Execute torch.compile
    - Call torch.compiler.save_cache_artifacts()
    """
    from ._cache import CacheArtifactManager, CacheInfo

    return CacheArtifactManager.serialize()
