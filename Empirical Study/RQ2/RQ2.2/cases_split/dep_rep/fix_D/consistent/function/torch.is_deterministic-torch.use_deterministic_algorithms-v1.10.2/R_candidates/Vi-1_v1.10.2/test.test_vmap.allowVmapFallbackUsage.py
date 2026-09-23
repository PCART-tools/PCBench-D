def allowVmapFallbackUsage(fn):
    fn._allow_vmap_fallback_usage = True
    return fn
