    def key_release(self, event):
        KeyEvent("key_release_event", self,
                 self._get_key(event), *self._event_mpl_coords(event),
                 guiEvent=event)._process()
