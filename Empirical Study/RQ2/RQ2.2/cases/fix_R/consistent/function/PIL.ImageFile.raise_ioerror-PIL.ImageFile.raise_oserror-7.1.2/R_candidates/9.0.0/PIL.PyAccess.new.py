def new(img, readonly=False):
    access_type = mode_map.get(img.mode, None)
    if not access_type:
        logger.debug("PyAccess Not Implemented: %s", img.mode)
        return None
    return access_type(img, readonly)
