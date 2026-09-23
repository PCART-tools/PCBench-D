    def _key_press(self, event):
        if event.key is None or self.keypresslock.locked():
            return

        name = self._keys.get(event.key, None)
        if name is None:
            return
        self.trigger_tool(name, canvasevent=event)
