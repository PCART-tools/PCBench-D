    def _handle_key(self, event):
        KeyEvent(event['type'] + '_event', self,
                 _handle_key(event['key']), *self._last_mouse_xy,
                 guiEvent=event.get('guiEvent'))._process()
