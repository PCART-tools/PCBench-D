    def home(self):
        """
        Push the first element onto the top of the stack.

        The first element is returned.
        """
        if not len(self._elements):
            return
        self.push(self._elements[0])
        return self()
