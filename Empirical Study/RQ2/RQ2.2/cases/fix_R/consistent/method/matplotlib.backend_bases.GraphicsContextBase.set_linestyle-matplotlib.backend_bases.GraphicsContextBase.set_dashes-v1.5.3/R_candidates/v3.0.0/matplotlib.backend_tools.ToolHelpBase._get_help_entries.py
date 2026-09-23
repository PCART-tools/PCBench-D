    def _get_help_entries(self):
        entries = []
        for name, tool in sorted(self.toolmanager.tools.items()):
            if not tool.description:
                continue
            entries.append((name, self._format_tool_keymap(name),
                            tool.description))
        return entries
