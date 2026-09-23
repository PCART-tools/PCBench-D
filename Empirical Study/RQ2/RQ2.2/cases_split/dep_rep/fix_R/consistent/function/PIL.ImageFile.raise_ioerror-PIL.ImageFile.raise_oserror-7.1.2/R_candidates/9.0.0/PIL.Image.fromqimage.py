def fromqimage(im):
    """Creates an image instance from a QImage image"""
    from . import ImageQt

    if not ImageQt.qt_is_installed:
        raise ImportError("Qt bindings are not installed")
    return ImageQt.fromqimage(im)
