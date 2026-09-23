    def key_press(self, event):
        KeyEvent("key_press_event", self,
                 self._get_key(event), *self._event_mpl_coords(event),
                 guiEvent=event)._process()
