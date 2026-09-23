    def release(self, event):
        if self._active == 'ZOOM':
            # When the mouse is released we reset the overlay and it
            # restores the former content to the window.
            if not self.retinaFix:
                self.wxoverlay.Reset()
                del self.wxoverlay
            else:
                del self.savedRetinaImage
                if self.prevZoomRect:
                    self.prevZoomRect.pop(0).remove()
                    self.prevZoomRect = None
                if self.zoomAxes:
                    self.zoomAxes = None
