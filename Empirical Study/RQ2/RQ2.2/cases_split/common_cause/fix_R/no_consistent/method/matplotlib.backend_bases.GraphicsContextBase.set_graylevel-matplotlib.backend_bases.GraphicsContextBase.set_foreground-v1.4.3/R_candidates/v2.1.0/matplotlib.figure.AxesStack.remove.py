    def remove(self, a):
        """Remove the axes from the stack."""
        Stack.remove(self, self._entry_from_axes(a))
