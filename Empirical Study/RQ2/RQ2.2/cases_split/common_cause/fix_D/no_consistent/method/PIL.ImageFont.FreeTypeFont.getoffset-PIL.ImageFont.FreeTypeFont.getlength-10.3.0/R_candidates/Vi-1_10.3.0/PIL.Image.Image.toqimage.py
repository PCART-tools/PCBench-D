    def toqimage(self):
        """Returns a QImage copy of this image"""
        from . import ImageQt

        if not ImageQt.qt_is_installed:
            msg = "Qt bindings are not installed"
            raise ImportError(msg)
        return ImageQt.toqimage(self)
