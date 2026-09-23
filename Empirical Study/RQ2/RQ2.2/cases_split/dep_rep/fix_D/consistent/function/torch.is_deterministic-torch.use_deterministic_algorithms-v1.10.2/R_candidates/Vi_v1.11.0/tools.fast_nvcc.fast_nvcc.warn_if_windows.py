def warn_if_windows() -> None:
    """
    Warn the user that using fast_nvcc on Windows might not work.
    """
    # use os.name instead of platform.system() because there is a
    # platform.py file in this directory, making it very difficult to
    # import the platform module from the Python standard library
    if os.name == 'nt':
        fast_nvcc_warn("untested on Windows, might not work; see this URL:")
        fast_nvcc_warn(url_vars)
