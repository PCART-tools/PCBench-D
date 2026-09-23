    def press(self, event):
        if self._active == 'ZOOM':
            if not self.retinaFix:
                self.wxoverlay = wx.Overlay()
            else:
                if event.inaxes is not None:
                    self.savedRetinaImage = self.canvas.copy_from_bbox(
                        event.inaxes.bbox)
                    self.zoomStartX = event.xdata
                    self.zoomStartY = event.ydata
                    self.zoomAxes = event.inaxes
