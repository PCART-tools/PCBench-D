    def contains(self, mouseevent):
        # docstring inherited.
        if self._contains is not None:
            return self._contains(self, mouseevent)
        return self.patch.contains(mouseevent)
