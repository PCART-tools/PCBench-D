@atexit.register
def move_cutlass_compiled_cache() -> None:
    """Move CUTLASS compiled cache file to the cache directory if it exists."""
    if "cutlass" not in sys.modules:
        return

    import cutlass  # type: ignore[import-not-found]

    if not os.path.exists(cutlass.CACHE_FILE):
        return

    try:
        filename = os.path.basename(cutlass.CACHE_FILE)
        shutil.move(cutlass.CACHE_FILE, os.path.join(cache_dir(), filename))
        log.debug("Moved CUTLASS compiled cache file to %s", cache_dir())
    except OSError as e:
        log.warning("Failed to move CUTLASS compiled cache file: %s", str(e))
