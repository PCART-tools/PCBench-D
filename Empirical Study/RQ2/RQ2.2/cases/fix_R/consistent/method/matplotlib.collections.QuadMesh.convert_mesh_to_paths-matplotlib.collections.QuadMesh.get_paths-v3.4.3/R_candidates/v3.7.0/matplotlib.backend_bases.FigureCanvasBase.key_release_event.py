    @_api.deprecated("3.6", alternative=(
        "callbacks.process('key_release_event', KeyEvent(...))"))
    def key_release_event(self, key, guiEvent=None):
        """
        Pass a `KeyEvent` to all functions connected to ``key_release_event``.
        """
        s = 'key_release_event'
        event = KeyEvent(
            s, self, key, self._lastx, self._lasty, guiEvent=guiEvent)
        self.callbacks.process(s, event)
        self._key = None
