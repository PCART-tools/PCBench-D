    def bubble(self, o):
        """
        raise *o* to the top of the stack and return *o*.  *o* must be
        in the stack
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
        for thiso in bubbles:
            self.push(o)
        return o
