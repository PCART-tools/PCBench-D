def should_allow_vmap_fallback_usage(fn):
    return getattr(fn, '_allow_vmap_fallback_usage', False)
