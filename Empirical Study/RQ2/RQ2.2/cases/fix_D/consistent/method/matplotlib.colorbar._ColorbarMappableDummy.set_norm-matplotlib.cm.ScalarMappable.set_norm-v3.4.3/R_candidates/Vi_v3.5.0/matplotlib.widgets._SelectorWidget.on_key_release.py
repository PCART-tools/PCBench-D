    def on_key_release(self, event):
        """Key release event handler and validator."""
        if self.active:
            key = event.key or ''
            for (state, modifier) in self.state_modifier_keys.items():
                if modifier in key:
                    self._state.discard(state)
            self._on_key_release(event)
