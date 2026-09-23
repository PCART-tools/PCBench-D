def _cutlass_path() -> str:
    if config.is_fbcode():
        from libfb.py import parutil

        return parutil.get_dir_path("cutlass-3-headers")
    else:
        return config.cuda.cutlass_dir
