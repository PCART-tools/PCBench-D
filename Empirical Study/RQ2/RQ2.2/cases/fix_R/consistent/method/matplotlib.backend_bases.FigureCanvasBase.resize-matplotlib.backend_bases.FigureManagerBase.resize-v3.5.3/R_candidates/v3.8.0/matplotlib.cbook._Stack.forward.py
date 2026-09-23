    def forward(self):
        """Move the position forward and return the current element."""
        self._pos = min(self._pos + 1, len(self._elements) - 1)
        return self()
