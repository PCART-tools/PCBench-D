    def toqpixmap(self):
        """Returns a QPixmap copy of this image"""
        from . import ImageQt

        if not ImageQt.qt_is_installed:
            msg = "Qt bindings are not installed"
            raise ImportError(msg)
        return ImageQt.toqpixmap(self)
