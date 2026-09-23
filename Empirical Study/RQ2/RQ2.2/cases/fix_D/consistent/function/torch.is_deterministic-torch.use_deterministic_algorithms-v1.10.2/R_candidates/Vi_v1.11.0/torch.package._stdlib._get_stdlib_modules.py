def _get_stdlib_modules():
    if sys.version_info.major == 3:
        if sys.version_info.minor == 6:
            return stdlib3_6
        if sys.version_info.minor == 7:
            return stdlib3_7
        if sys.version_info.minor == 8:
            return stdlib3_8
        if sys.version_info.minor == 9:
            return stdlib3_9

    raise RuntimeError(f"Unsupported Python version: {sys.version_info}")
