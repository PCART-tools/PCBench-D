    def keyPressEvent(self, event):
        key = self._get_key(event)
        if key is not None:
            FigureCanvasBase.key_press_event(self, key, guiEvent=event)
