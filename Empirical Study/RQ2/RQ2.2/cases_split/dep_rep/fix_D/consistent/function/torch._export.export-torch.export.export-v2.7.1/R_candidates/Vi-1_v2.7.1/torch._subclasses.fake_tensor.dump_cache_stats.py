@atexit.register
def dump_cache_stats() -> None:
    log.info("FakeTensor cache stats:")
    log.info("  cache_hits: %s", FakeTensorMode.cache_hits)
    log.info("  cache_misses: %s", FakeTensorMode.cache_misses)
    bypasses = FakeTensorMode.cache_bypasses
    if bypasses:
        log.info("  cache_bypasses:")
        width = max(len(k) for k in bypasses)
        for k, v in sorted(bypasses.items(), key=lambda i: -i[1]):
            log.info("    %-*s %s", width + 1, f"{k}:", v)
