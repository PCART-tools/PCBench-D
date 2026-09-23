    def keyPressEvent(self, event):
        key = self._get_key(event)
        if key is not None and self.figure is not None:
            KeyEvent("key_press_event", self,
                     key, *self.mouseEventCoords(),
                     guiEvent=event)._process()
