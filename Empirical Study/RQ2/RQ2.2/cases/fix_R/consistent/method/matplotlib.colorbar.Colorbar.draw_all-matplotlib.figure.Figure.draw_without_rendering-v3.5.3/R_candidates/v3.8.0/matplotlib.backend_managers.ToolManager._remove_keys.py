    def _remove_keys(self, name):
        for k in self.get_tool_keymap(name):
            del self._keys[k]
