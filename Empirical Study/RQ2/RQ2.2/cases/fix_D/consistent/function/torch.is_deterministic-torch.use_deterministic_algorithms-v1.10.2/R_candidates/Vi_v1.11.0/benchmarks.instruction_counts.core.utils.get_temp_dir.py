def get_temp_dir() -> str:
    global _TEMPDIR
    if _TEMPDIR is None:
        _TEMPDIR = _make_temp_dir(prefix="instruction_count_microbenchmarks", gc_dev_shm=True)
        atexit.register(shutil.rmtree, path=_TEMPDIR)
    return _TEMPDIR
