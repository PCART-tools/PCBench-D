def versions():
    """
    (pyCMS) Fetches versions.
    """

    return (VERSION, core.littlecms_version, sys.version.split()[0], Image.__version__)
