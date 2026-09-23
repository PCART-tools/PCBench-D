    def _frame_sink(self):
        """Return the place to which frames should be written."""
        return self._proc.stdin
