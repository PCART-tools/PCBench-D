    def mouseMoveEvent(self, event):
        MouseEvent("motion_notify_event", self,
                   *self.mouseEventCoords(event),
                   modifiers=self._mpl_modifiers(),
                   guiEvent=event)._process()
