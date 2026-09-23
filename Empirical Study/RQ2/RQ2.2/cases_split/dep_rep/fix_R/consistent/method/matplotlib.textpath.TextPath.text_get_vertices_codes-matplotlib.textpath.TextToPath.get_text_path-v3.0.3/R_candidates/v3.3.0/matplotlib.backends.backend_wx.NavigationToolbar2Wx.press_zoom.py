    def press_zoom(self, event):
        super().press_zoom(event)
        if self.mode.name == 'ZOOM':
            if not self._retinaFix:
                self._wxoverlay = wx.Overlay()
            else:
                if event.inaxes is not None:
                    self._savedRetinaImage = self.canvas.copy_from_bbox(
                        event.inaxes.bbox)
                    self._zoomStartX = event.xdata
                    self._zoomStartY = event.ydata
                    self._zoomAxes = event.inaxes
