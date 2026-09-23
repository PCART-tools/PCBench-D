def fromqpixmap(im):
    """Creates an image instance from a QPixmap image"""
    from . import ImageQt

    if not ImageQt.qt_is_installed:
        raise ImportError("Qt bindings are not installed")
    return ImageQt.fromqpixmap(im)
