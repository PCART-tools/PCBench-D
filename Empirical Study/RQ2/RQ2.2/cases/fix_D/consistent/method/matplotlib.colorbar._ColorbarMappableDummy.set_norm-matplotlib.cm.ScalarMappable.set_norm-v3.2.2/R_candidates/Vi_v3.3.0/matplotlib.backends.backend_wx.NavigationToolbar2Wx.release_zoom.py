    def release_zoom(self, event):
        super().release_zoom(event)
        if self.mode.name == 'ZOOM':
            # When the mouse is released we reset the overlay and it
            # restores the former content to the window.
            if not self._retinaFix:
                self._wxoverlay.Reset()
                del self._wxoverlay
            else:
                del self._savedRetinaImage
                if self._prevZoomRect:
                    self._prevZoomRect.pop(0).remove()
                    self._prevZoomRect = None
                if self._zoomAxes:
                    self._zoomAxes = None
