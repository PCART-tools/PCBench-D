def version():
    """Returns the version of cuDNN"""
    if not _init():
        return None
    return __cudnn_version
