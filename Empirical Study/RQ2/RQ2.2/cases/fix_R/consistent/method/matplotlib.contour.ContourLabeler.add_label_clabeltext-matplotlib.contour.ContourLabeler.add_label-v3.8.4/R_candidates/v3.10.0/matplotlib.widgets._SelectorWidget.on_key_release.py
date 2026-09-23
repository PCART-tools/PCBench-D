    def on_key_release(self, event):
        """Key release event handler and validator."""
        if self.active:
            key = event.key or ''
            for (state, modifier) in self._state_modifier_keys.items():
                # 'rotate' is changing _state on press and is not removed
                # from _state when releasing
                if modifier in key.split('+') and state != 'rotate':
                    self._state.discard(state)
            self._on_key_release(event)
