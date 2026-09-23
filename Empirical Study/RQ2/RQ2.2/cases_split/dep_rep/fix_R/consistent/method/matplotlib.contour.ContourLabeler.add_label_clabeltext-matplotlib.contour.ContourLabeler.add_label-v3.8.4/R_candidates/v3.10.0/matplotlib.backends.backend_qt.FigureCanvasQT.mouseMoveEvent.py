    def mouseMoveEvent(self, event):
        if self.figure is None:
            return
        MouseEvent("motion_notify_event", self,
                   *self.mouseEventCoords(event),
                   buttons=self._mpl_buttons(event.buttons()),
                   modifiers=self._mpl_modifiers(),
                   guiEvent=event)._process()
