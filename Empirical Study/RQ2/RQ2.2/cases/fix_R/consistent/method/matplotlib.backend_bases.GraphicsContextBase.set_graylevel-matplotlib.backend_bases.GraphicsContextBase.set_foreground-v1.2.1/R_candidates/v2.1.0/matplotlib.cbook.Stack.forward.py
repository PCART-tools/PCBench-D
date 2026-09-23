    def forward(self):
        """move the position forward and return the current element"""
        n = len(self._elements)
        if self._pos < n - 1:
            self._pos += 1
        return self()
