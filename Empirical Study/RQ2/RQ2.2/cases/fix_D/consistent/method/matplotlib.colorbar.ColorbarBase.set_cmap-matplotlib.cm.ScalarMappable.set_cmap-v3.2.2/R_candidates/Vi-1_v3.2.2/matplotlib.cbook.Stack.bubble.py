    def bubble(self, o):
        """
        Raise *o* to the top of the stack.  *o* must be present in the stack.

        *o* is returned.
        """
        if o not in self._elements:
            raise ValueError('Unknown element o')
        old = self._elements[:]
        self.clear()
        bubbles = []
        for thiso in old:
            if thiso == o:
                bubbles.append(thiso)
            else:
                self.push(thiso)
        for _ in bubbles:
            self.push(o)
        return o
