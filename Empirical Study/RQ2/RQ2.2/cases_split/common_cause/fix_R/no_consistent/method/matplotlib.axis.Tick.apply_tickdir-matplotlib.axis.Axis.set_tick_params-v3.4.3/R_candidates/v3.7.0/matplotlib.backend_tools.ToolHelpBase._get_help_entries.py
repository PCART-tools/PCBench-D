    def _get_help_entries(self):
        return [(name, self._format_tool_keymap(name), tool.description)
                for name, tool in sorted(self.toolmanager.tools.items())
                if tool.description]
