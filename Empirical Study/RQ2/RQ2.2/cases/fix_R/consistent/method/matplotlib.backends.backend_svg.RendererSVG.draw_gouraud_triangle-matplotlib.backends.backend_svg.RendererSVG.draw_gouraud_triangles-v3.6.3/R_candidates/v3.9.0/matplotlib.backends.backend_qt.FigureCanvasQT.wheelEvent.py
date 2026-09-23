    def wheelEvent(self, event):
        # from QWheelEvent::pixelDelta doc: pixelDelta is sometimes not
        # provided (`isNull()`) and is unreliable on X11 ("xcb").
        if (event.pixelDelta().isNull()
                or QtWidgets.QApplication.instance().platformName() == "xcb"):
            steps = event.angleDelta().y() / 120
        else:
            steps = event.pixelDelta().y()
        if steps and self.figure is not None:
            MouseEvent("scroll_event", self,
                       *self.mouseEventCoords(event), step=steps,
                       modifiers=self._mpl_modifiers(),
                       guiEvent=event)._process()
