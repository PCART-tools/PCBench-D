def pre_fork_setup():
    """
    Setup that must be done prior to forking with a process pool.
    """
    # ensure properties have been calculated before processes
    # are forked
    caching_device_properties()

    # Computing the triton key can be slow. If we call it before fork,
    # it will be cached for the forked subprocesses.
    try:
        from triton.compiler.compiler import triton_key

        triton_key()
    except ImportError:
        # Triton might not be installed or might be an old version.
        pass
