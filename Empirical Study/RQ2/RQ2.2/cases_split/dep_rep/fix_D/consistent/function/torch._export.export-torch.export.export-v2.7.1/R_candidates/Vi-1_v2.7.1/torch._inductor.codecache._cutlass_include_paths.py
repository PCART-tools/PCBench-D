def _cutlass_include_paths() -> list[str]:
    if config.is_fbcode():
        from libfb.py import parutil

        cutlass_path = parutil.get_dir_path("cutlass-3-headers")
    else:
        cutlass_path = config.cuda.cutlass_dir
    return [
        # Use realpath to get canonical absolute paths, in order not to mess up cache keys
        os.path.realpath(os.path.join(cutlass_path, "include")),
        os.path.realpath(os.path.join(cutlass_path, "tools/library/include")),
        os.path.realpath(os.path.join(cutlass_path, "tools/library/src")),
        os.path.realpath(os.path.join(cutlass_path, "tools/util/include")),
    ]
