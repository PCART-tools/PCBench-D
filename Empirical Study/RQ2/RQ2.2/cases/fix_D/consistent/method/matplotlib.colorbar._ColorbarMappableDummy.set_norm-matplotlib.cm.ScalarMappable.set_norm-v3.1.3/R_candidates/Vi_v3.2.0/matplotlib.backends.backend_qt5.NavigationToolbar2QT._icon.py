    def _icon(self, name, color=None):
        if is_pyqt5():
            name = name.replace('.png', '_large.png')
        pm = QtGui.QPixmap(os.path.join(self.basedir, name))
        if hasattr(pm, 'setDevicePixelRatio'):
            pm.setDevicePixelRatio(self.canvas._dpi_ratio)
        if color is not None:
            mask = pm.createMaskFromColor(QtGui.QColor('black'),
                                          QtCore.Qt.MaskOutColor)
            pm.fill(color)
            pm.setMask(mask)
        return QtGui.QIcon(pm)
