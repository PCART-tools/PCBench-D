    def key_press_event(self, widget, event):
        key = self._get_key(event)
        FigureCanvasBase.key_press_event(self, key, guiEvent=event)
        return True  # stop event propagation
