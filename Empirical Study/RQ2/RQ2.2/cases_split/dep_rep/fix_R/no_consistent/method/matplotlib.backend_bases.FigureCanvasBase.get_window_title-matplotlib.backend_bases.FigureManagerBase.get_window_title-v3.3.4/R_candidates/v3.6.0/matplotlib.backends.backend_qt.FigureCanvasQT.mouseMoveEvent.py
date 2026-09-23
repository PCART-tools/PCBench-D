    def mouseMoveEvent(self, event):
        MouseEvent("motion_notify_event", self,
                   *self.mouseEventCoords(event),
                   guiEvent=event)._process()
