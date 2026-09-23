    def bubble(self, o):
        """
        Raise all references of *o* to the top of the stack, and return it.

        Raises
        ------
        ValueError
            If *o* is not in the stack.
        """
        if o not in self._elements:
            raise ValueError('Given element not contained in the stack')
        old_elements = self._elements.copy()
        self.clear()
        top_elements = []
        for elem in old_elements:
            if elem == o:
                top_elements.append(elem)
            else:
                self.push(elem)
        for _ in top_elements:
            self.push(o)
        return o
