def check_feature(feature):
    """
    Checks if a feature is available.

    :param feature: The feature to check for.
    :returns: ``True`` if available, ``False`` if unavailable, ``None`` if unknown.
    :raises ValueError: If the feature is not defined in this version of Pillow.
    """
    if feature not in features:
        raise ValueError(f"Unknown feature {feature}")

    module, flag, ver = features[feature]

    try:
        imported_module = __import__(module, fromlist=["PIL"])
        return getattr(imported_module, flag)
    except ImportError:
        return None
