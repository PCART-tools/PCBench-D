    def wheelEvent(self, event):
        x, y = self.mouseEventCoords(self._get_position(event))
        # from QWheelEvent::pixelDelta doc: pixelDelta is sometimes not
        # provided (`isNull()`) and is unreliable on X11 ("xcb").
        if (event.pixelDelta().isNull()
                or QtWidgets.QApplication.instance().platformName() == "xcb"):
            steps = event.angleDelta().y() / 120
        else:
            steps = event.pixelDelta().y()
        if steps:
            FigureCanvasBase.scroll_event(
                self, x, y, steps, guiEvent=event)
