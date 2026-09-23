    def remove(self, o):
        """
        Remove *o* from the stack.

        Raises
        ------
        ValueError
            If *o* is not in the stack.
        """
        if o not in self._elements:
            raise ValueError('Given element not contained in the stack')
        old_elements = self._elements.copy()
        self.clear()
        for elem in old_elements:
            if elem != o:
                self.push(elem)
