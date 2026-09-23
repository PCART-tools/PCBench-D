def build_info() -> dict[str, Any]:
    """
    Return a dict with Polars build information.

    If Polars was compiled with "build_info" feature gate return the full build info,
    otherwise only version is included. The full build information dict contains
    the following keys ['build', 'info-time', 'dependencies', 'features', 'host',
    'target', 'git', 'version'].
    """
    return _build_info_
