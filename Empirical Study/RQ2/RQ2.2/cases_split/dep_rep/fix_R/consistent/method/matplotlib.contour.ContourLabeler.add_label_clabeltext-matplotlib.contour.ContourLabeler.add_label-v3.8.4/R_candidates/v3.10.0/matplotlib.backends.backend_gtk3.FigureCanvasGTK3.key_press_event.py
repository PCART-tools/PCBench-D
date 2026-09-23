    def key_press_event(self, widget, event):
        KeyEvent("key_press_event", self,
                 self._get_key(event), *self._mpl_coords(),
                 guiEvent=event)._process()
        return True  # stop event propagation
