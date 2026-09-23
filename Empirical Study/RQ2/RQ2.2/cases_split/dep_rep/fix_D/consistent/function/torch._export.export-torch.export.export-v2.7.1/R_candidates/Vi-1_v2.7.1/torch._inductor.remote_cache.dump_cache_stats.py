@atexit.register
def dump_cache_stats() -> None:
    if not log.isEnabledFor(logging.INFO):
        return

    import io

    out = io.StringIO()

    if not cache_stats._stats:
        print(" None", file=out)
    else:
        print(file=out)
        for k, v in sorted(cache_stats._stats.items()):
            print(f"  {k}: {v}", file=out)

    log.info("Cache Metrics:%s", out.getvalue())
