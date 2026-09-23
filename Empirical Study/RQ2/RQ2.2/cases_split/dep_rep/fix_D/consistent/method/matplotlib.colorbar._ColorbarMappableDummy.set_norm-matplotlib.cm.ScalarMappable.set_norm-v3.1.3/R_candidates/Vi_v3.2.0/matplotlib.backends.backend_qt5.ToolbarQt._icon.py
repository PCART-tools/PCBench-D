    def _icon(self, name):
        pm = QtGui.QPixmap(name)
        if hasattr(pm, 'setDevicePixelRatio'):
            pm.setDevicePixelRatio(self.toolmanager.canvas._dpi_ratio)
        return QtGui.QIcon(pm)
