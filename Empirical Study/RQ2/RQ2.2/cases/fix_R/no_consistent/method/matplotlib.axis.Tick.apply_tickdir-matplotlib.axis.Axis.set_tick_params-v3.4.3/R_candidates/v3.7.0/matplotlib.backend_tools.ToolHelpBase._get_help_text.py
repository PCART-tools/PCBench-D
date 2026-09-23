    def _get_help_text(self):
        entries = self._get_help_entries()
        entries = ["{}: {}\n\t{}".format(*entry) for entry in entries]
        return "\n".join(entries)
