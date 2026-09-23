    def _icon(self, name):
        """
        Construct a `.QIcon` from an image file *name*, including the extension
        and relative to Matplotlib's "images" data directory.
        """
        if QtCore.qVersion() >= '5.':
            name = name.replace('.png', '_large.png')
        pm = QtGui.QPixmap(str(cbook._get_data_path('images', name)))
        _setDevicePixelRatioF(pm, _devicePixelRatioF(self))
        if self.palette().color(self.backgroundRole()).value() < 128:
            icon_color = self.palette().color(self.foregroundRole())
            mask = pm.createMaskFromColor(QtGui.QColor('black'),
                                          QtCore.Qt.MaskOutColor)
            pm.fill(icon_color)
            pm.setMask(mask)
        return QtGui.QIcon(pm)
