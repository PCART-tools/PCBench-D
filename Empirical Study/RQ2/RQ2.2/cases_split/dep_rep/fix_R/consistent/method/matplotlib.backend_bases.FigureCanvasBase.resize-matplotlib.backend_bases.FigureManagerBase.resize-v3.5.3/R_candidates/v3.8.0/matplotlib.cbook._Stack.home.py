    def home(self):
        """
        Push the first element onto the top of the stack.

        The first element is returned.
        """
        return self.push(self._elements[0]) if self._elements else None
