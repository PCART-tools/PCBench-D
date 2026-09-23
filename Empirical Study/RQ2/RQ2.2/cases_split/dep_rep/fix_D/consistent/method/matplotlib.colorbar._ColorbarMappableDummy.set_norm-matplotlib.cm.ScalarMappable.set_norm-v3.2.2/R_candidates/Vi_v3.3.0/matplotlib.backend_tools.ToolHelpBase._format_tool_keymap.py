    def _format_tool_keymap(self, name):
        keymaps = self.toolmanager.get_tool_keymap(name)
        return ", ".join(self.format_shortcut(keymap) for keymap in keymaps)
