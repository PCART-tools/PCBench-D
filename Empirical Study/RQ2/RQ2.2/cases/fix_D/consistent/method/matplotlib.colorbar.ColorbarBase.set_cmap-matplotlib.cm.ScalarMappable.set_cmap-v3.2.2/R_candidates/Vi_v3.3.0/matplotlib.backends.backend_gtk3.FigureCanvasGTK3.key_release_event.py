    def key_release_event(self, widget, event):
        key = self._get_key(event)
        FigureCanvasBase.key_release_event(self, key, guiEvent=event)
        return True  # stop event propagation
