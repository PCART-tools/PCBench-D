    @property
    def _icon_extension(self):
        if is_pyqt5():
            return '_large.png'
        return '.png'
